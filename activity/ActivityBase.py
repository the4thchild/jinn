import g
from feedback.LogLevels import LogLevels
from loader.UrlDownloader import UrlDownloader
from helpers.FileSystemHelper import FileSystemHelper
import hashlib
from helpers.CompressionHelper import CompressionHelper

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
    
    """
    Provides the ability to load properties from configuration file
    """
    def loadProperties(self, properties):
        self.properties = properties;
        #g.feedback.log(LogLevels.DEBUG, properties)
    
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
    """
    def doDownload(self, url, file = None):
        if file is None:
            file = hashlib.md5(url).hexdigest()
        if self.exists(file):
            self.delete(file)
        downloader = UrlDownloader(url)
        return downloader.download(file)