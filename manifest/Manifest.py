import sys
from loader.FileLoader import FileLoader
from loader.UrlLoader import UrlLoader
from manifest.exceptions import ManifestException
from JinnVersion import JinnVersion
from resource.ResourceWrapper import ResourceWrapper
from action.ActionWrapper import ActionWrapper
from env.enums import *
from helpers.FileSystemHelper import FileSystemHelper
import g
from feedback.LogLevels import LogLevels
import json

class Manifest(FileSystemHelper):
    
    def __init__(self, os, arch, location, is_url = True, isInstalled = False):
        self.jinn = None
        self.description = ""
        self.resources = []
        self.actions = []
        self.os = os
        self.arch = arch
        
        g.feedback.log(LogLevels.DEBUG, "Manifest initialised from %s. OS: %s, Arch: %s" % (location, self.os, self.arch))
        
        self.load(location, is_url, isInstalled)
    
    """
    Loads data for this manifest from a specific location, then calls to parse it
    """
    def load(self, location, is_url, isInstalled):
        
        g.feedback.log(LogLevels.DEBUG, "Loading from %s" % location)
        g.feedback.log(LogLevels.DEBUG, "Is installed? %s" % str(isInstalled))
        
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
        g.feedback.log(LogLevels.DEBUG, "Reading version data")
        self.jinn = JinnVersion(self.data["Jinn"])
    
    """
    Load out the description
    """
    def readDescription(self):
        g.feedback.log(LogLevels.DEBUG, "Reading description")
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
        g.feedback.log(LogLevels.DEBUG, "Loading resources")
        try:
            i = 0
            dataResources = self.data["Resources"]
            for k in dataResources.keys():
                g.feedback.log(LogLevels.DEBUG, "Found resource with ID %s" % k)
                res = ResourceWrapper(k, self, dataResources[k], self.os, self.arch)
                if res.checkConditions():
                    g.feedback.log(LogLevels.DEBUG, "Conditions met for resource %s" % k)
                    g.feedback.log(LogLevels.DEBUG, "Setting installed status of %s to %s" % (k, str(isInstalled)))
                    res.setInstalled(isInstalled)
                    self.resources.append(res)
                else:
                    g.feedback.log(LogLevels.DEBUG, "Conditions not met for resource %s" % k)
                i += 1
            if i < 1:
                raise ManifestException("The manifest must contain at least one resource")
        except KeyError:
            raise ManifestException("The manifest file does not contain any resources")
    
    """
    Load actions from the data
    """
    def loadActions(self):
        g.feedback.log(LogLevels.DEBUG, "Loading actions")
        try:
            dataActions = self.data["Actions"]
            for k in dataActions.keys():
                g.feedback.log(LogLevels.DEBUG, "Found action with ID %s" % k)
                action = ActionWrapper(k, self, dataActions[k], self.os, self.arch)
                if action.checkConditions():
                    g.feedback.log(LogLevels.DEBUG, "Conditions met for action %s" % k)
                    self.actions.append(action)
                else:
                    g.feedback.log(LogLevels.DEBUG, "Conditions not met for action %s" % k)
        except KeyError:
            raise ManifestException("The manifest file does not contain any actions")
    
    """
    Run the default action
    Returns false if no default action
    """
    def runDefaultAction(self, args):
        g.feedback.log(LogLevels.DEBUG, "Running default action")
        for action in self.actions:
            if action.default:
                g.feedback.log(LogLevels.DEBUG, "The default action run is %s" % action.id)
                return action.run(args)
        g.feedback.log(LogLevels.DEBUG, "No default action found")
        return False
    
    """
    Run the specified action
    """
    def runAction(self, actionName, args):
        g.feedback.log(LogLevels.DEBUG, "Running action %s with args %s" % (actionName, args))
        for action in self.actions:
            if action.id == actionName:
                return action.run(args)
        return False

    """
    Returns the name of the manifest file
    """
    def getManifestFile(self):
        mfile = ".jinn" + self.getDirectorySeparator() + "current_manifest.json"
        g.feedback.log(LogLevels.DEBUG, "Manifest file is %s" % mfile)
        return mfile

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
        g.feedback.log(LogLevels.DEBUG, "Installing resources")
        for res in self.resources:
            if not res.doInstall():
                g.feedback.log(LogLevels.DEBUG, "Failed to install resource with ID %s" % res.id)
                return False
        return True
    
    """
    Set the install status of resources if they are
    already installed at the right version
    """
    def setInstallStatus(self, old_resources):
        for old_res in old_resources:
            new_res = self.getResourceForId(old_res.id)
            if new_res is not None:
                if new_res.version == old_res.version:
                    g.feedback.log(LogLevels.DEBUG, "Updating installed status of %s to %s" % (new_res.id, str(old_res.isInstalled)))
                    new_res.setInstalled(old_res.isInstalled)
        return True
    
    """
    Installs resources that are new in me from the old_resources
    """
    def installNewResources(self, old_resources):
        for res in self.resources:
            old_resource = self.getResourceForId(res.id, old_resources)
            if old_resource is None:
                g.feedback.log(LogLevels.DEBUG, "Resource with ID %s is new, so installing" % res.id)
                if not res.doInstall():
                    g.feedback.log(LogLevels.DEBUG, "Installing new resource with ID %s failed" % res.id)
                    return False
        return True
    
    """
    Uninstalls resources that were in old_resources but are not in me
    """
    def uninstallRemovedResources(self, old_resources):
        for res in old_resources:
            new_resource = self.getResourceForId(res.id)
            if new_resource is None:
                g.feedback.log(LogLevels.DEBUG, "Resource with ID %s is removed, so uninstalling" % res.id)
                if not res.doUninstall():
                    g.feedback.log(LogLevels.DEBUG, "Uninstalling old resource with ID %s failed" % res.id)
                    return False
        return True
    
    """
    For the resources that are in both me and old_resources, if the
    version has changed, update that resource
    """
    def updateResources(self, old_resources):
        for old_res in old_resources:
            new_res = self.getResourceForId(old_res.id)
            if new_res is not None:
                if new_res.version != old_res.version and new_res.isUpdatable(old_res):
                    g.feedback.log(LogLevels.DEBUG, "Resource with ID %s is changing version from %s to %s" % (new_res.id, old_res.version, new_res.version))
                    if not old_res.doUninstall():
                        g.feedback.log(LogLevels.DEBUG, "Failed to uninstall updating resource with ID %s" % new_res.id)
                        return False
                    # Install new one
                    if not new_res.doInstall():
                        g.feedback.log(LogLevels.DEBUG, "Failed to install updating resource with ID %s" % new_res.id)
                        return False
                    # Install the dependents that were removed during the uninstall
                    if not new_res.installDependents():
                        g.feedback.log(LogLevels.DEBUG, "Failed to install dependents of updating resource with ID %s" % new_res.id)
                        return False
        return True
    
    """
    Uninstall all of the resources
    """
    def uninstallResources(self):
        g.feedback.log(LogLevels.DEBUG, "Uninstalling all resources")
        for res in self.resources:
            if not res.doUninstall():
                g.feedback.log(LogLevels.DEBUG, "Uninstalling resource with ID %s failed" % res.id)
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
    def getResourceForId(self, i, resources = None):
        if resources is None:
            resources = self.resources
        for res in resources:
            if res.getId() == i:
                return res
        return None
