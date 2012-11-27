import g
from feedback.LogLevels import LogLevels
from loader.UrlDownloader import UrlDownloader
from helpers.FileSystemHelper import FileSystemHelper
import hashlib
from helpers.CompressionHelper import CompressionHelper
from activity.exceptions import RequiredPropertyNotFound
from env.enums import OperatingSystem
from env.enums import Architecture

"""
A base class for Resources and Actions
Defines methods that these types, through
ActionBase and ResourceBase, can implement
"""
class ActivityBase(CompressionHelper):
    
    # Properties of this activity
    properties = None
    
    # The OS context we are running in
    os = None
    
    # The architecture context we are running in
    arch = None
    
    # The manifest of the installation
    manifest = None
    
    def loadManifest(self, manifest):
        self.manifest = manifest
    
    """
    Provides the ability to load properties from configuration file
    """
    def loadProperties(self, properties):
        self.properties = properties;
        #g.feedback.log(LogLevels.DEBUG, properties)
        
    """
    Return a property from the properties
    Allows specification for whether it is required or not
    If required and not available, throws exception
    If not required and not available, returns None
    """
    def getProperty(self, name, required = True):
        if name in self.properties:
            prop = self.properties[name]
            # See if property is a dict so must be a special object
            if type(prop) is dict:
                # Platform property type, so need to return the right one
                if "Platform" in prop:
                    plat = prop["Platform"]
                    # Do we have the OS
                    myos = OperatingSystem().getOperatingSystem(self.os)
                    if myos in plat:
                        opsys = plat[myos]
                        # Do we have the architecture too
                        myarch = Architecture().getArchitecture(self.arch)
                        if myarch in opsys:
                            # If we have the platform and architecture, return the value
                            return opsys[myarch]
                    if "Default" in plat:
                        return plat["Default"]
            return prop
        if required:
            raise RequiredPropertyNotFound(name)
        else:
            return None
    
    """
    Return the type string this Activity corresponds to
    """
    def getType(self):
        return None
    
    """
    Initialises the activity with the os and architecture we are running under
    """
    def __init__(self, os, arch):
        self.os = os
        self.arch = arch
        
    """
    Helper function which does a download from a URL to a file
    If no path specified, goes to the project root
    If no name specified, falls back to a name from the URL. If that is not available, uses an MD5 of the URL
    """
    def doDownload(self, url, path, name):
        if path is None:
            path = "."
        if name is None:
            u,name = url.rsplit("/", 1)
            if len(name) < 1:
                name = hashlib.md5(url).hexdigest()
        fullPath = path + self.getDirectorySeparator() + name
        if self.exists(fullPath):
            self.delete(fullPath)
        downloader = UrlDownloader(url)
        return downloader.download(fullPath)