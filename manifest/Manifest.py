import sys
from loader.FileLoader import FileLoader
from loader.UrlLoader import UrlLoader
from manifest.exceptions import ManifestException
from JinnVersion import JinnVersion
from resource.ResourceWrapper import ResourceWrapper
from action.ActionWrapper import ActionWrapper
from env.enums import *
from helpers.FileSystemHelper import FileSystemHelper
import json

class Manifest(FileSystemHelper):
    
    def __init__(self, location, is_url = True, isInstalled = False):
        self.jinn = None
        self.description = ""
        self.resources = []
        self.actions = []
        
        self.load(location, is_url, isInstalled)
    
    """
    Loads data for this manifest from a specific location, then calls to parse it
    """
    def load(self, location, is_url, isInstalled):
        # TODO: Fix this
        if is_url:
            l = UrlLoader(location)
            data = l.read(True)
        else:
            l = FileLoader(location)
            data = l.read(True)
        if data is None:
            raise ManifestException("Unable to load data from the specified source")
        self.data = data;
        self.parseData(isInstalled)
        
    """
    Parses a generic data structure for this manifest
    """
    def parseData(self, isInstalled):
        self.readVersionData()
        self.readDescription()
        self.loadResources(isInstalled)
        self.loadActions()
        
    """
    Check the manifest version string is valid
    """
    def readVersionData(self):
        self.jinn = JinnVersion(self.data["Jinn"])
    
    """
    Load out the description
    """
    def readDescription(self):
        try:
            self.description = self.data["Description"]
        except KeyError:
            raise ManifestException("The manifest file does not contain a description")
        if self.description == None or len(self.description) < 1:
            raise ManifestException("You must provide a description of this manifest")
    
    """
    Load resources from the data
    """
    def loadResources(self, isInstalled):
        try:
            i = 0
            dataResources = self.data["Resources"]
            for k in dataResources.keys():
                res = ResourceWrapper(k, self, dataResources[k], OperatingSystem.LIN, Architecture.x64)
                if res.checkConditions():
                    res.setInstalled(isInstalled)
                    self.resources.append(res)
                i += 1
            if i < 1:
                raise ManifestException("The manifest must contain at least one resource")
        except KeyError:
            raise ManifestException("The manifest file does not contain any resources")
    
    """
    Load actions from the data
    """
    def loadActions(self):
        try:
            dataActions = self.data["Actions"]
            for k in dataActions.keys():
                action = ActionWrapper(k, self, dataActions[k], OperatingSystem.LIN, Architecture.x64)
                if action.checkConditions():
                    self.actions.append(action)
        except KeyError:
            raise ManifestException("The manifest file does not contain any actions")
    
    """
    Run the default action
    Returns false if no default action
    """
    def runDefaultAction(self):
        for action in self.actions:
            if action.default:
                return action.run()
        return False
    
    """
    Run the specified action
    """
    def runAction(self, actionName):
        for action in self.actions:
            if action.id == actionName:
                return action.run()
        return False

    """
    Returns the name of the manifest file
    """
    def getManifestFile(self):
        return ".jinn" + self.getDirectorySeparator() + "current_manifest.json"

    """
    Save the raw manifest data to the manifest fil
    """
    def save(self):
        if not self.delete(self.getManifestFile()):
            return False
        return self.saveToFile(self.getManifestFile(), json.dumps(self.data))
    
    """
    Installs all of the resources
    """
    def installResources(self):
        for res in self.resources:
            if not res.doInstall():
                return False
        return True
    
    """
    Installs resources that are new in me from the old_resources
    """
    def installNewResources(self, old_resources):
        pass
    
    """
    Uninstalls resources that were in old_resources but are not in me
    """
    def uninstallRemovedResources(self, old_resources):
        pass
    
    """
    For the resources that are in both me and old_resources, if the
    version has changed, update that resource
    """
    def updateResources(self, old_resources):
        pass
    
    """
    Uninstall all of the resources
    """
    def uninstallResources(self):
        for res in self.resources:
            if not res.doUninstall():
                return False
        return True
    
    """
    Helper which returns a resource which has a specific type
    Returns the inner type, not the wrapper!
    """
    def getResourceForType(self, t):
        for res in self.resources:
            if res.type.getType() == t:
                return res
        return None
            
    """
    Returns a resource given its ID
    Returns the wrapper
    """
    def getResourceForId(self, i):
        for res in self.resources:
            if res.getId() == i:
                return res
        return None
