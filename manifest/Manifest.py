import sys
from loader.FileLoader import FileLoader
from loader.UrlLoader import UrlLoader
from manifest.exceptions import ManifestException
from JinnVersion import JinnVersion
from resource.ResourceWrapper import ResourceWrapper
from action.ActionWrapper import ActionWrapper
from env.enums import *

class Manifest:
    
    # Versioning information
    jinn = None
    
    # Description of this jinn
    description = ""
    
    # Resources in the jinn
    resources = []
    
    # Actions in the jinn
    actions = []
    
    """
    Loads data for this manifest from a specific location, then calls to parse it
    """
    def load(self, location, is_url):
        if is_url:
            l = UrlLoader(location)
            data = l.read(True)
        else:
            l = FileLoader(location)
            data = l.read(True)
        if data is None:
            raise ManifestException("Unable to load data from the specified source")
        self.data = data;
        self.parseData()
        
    """
    Parses a generic data structure for this manifest
    """
    def parseData(self):
        self.readVersionData()
        self.readDescription()
        self.loadResources()
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
    def loadResources(self):
        try:
            i = 0
            dataResources = self.data["Resources"]
            for k in dataResources.keys():
                self.resources.append(ResourceWrapper(dataResources[k], OperatingSystem.LIN, Architecture.x64))
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
                self.actions.append(ActionWrapper(dataActions[k], OperatingSystem.LIN, Architecture.x64))
        except KeyError:
            raise ManifestException("The manifest file does not contain any actions")
    
    def __init__(self, location, is_url = True):
        self.load(location, is_url)

"""
Main function that is run when the code is started from this file
Running from this file picks up the first argument as the file to load,
downloads and parses it, and then reports on whether it was successfully loaded.
"""
def main():
    if len(sys.argv) < 2:
        print "You must provide an argument which is the relative name of a file to load"
        return 1
    print Manifest(sys.argv[1], False)
    print "Loaded from %s successfully" % sys.argv[1]
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)