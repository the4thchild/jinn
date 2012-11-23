import sys
import inspect
import g
from exceptions import *
from feedback.LogLevels import LogLevels
from env.enums import OperatingSystem, Architecture

"""
General code which applies to all activity wrappers
"""
class ActivityWrapper(object):
    
    # The manifest this activity is in
    manifest = None
    
    # The data for the activity (from config file)
    data = None
    
    # The type of this activity
    type = None
    
    # The name of this activity
    name = None
    
    # Description of the activity
    description = ""
    
    # Conditions of the activity
    conditions = None
    
    # The OS in use
    os = None
    
    # The architecture in use
    arch = None
    
    """
    Helper function which loads all the classes in this module,
    searches for ones with getType methods, and tries to find the
    one that matches the type given as input, returning an instance
    of it
    """
    def getClass(self, module, desiredType):
        clazzes = inspect.getmembers(sys.modules[module], inspect.isclass)
        for clazzdef in clazzes:
            clazz = clazzdef[1]
            obj = clazz(self.os, self.arch)
            try:
                attr = getattr(obj, "getType")
                if callable(attr):
                    clazztype = obj.getType()
                    if clazztype == desiredType:
                        return obj
            except:
                pass
        raise ActivityNotFoundException("Unable to load action for type %s" % desiredType)
    
    """
    Load helper for getting common stuff 
    """
    def load(self):
        self.name = self.data["Name"]
        if "Description" in self.data:
                self.description = self.data["Description"]
        self.properties = self.data["Properties"]
        if "Conditions" in self.data:
            self.conditions = self.data["Conditions"]
    
    """
    Helper to load a properties object
    """
    def loadPropertiesObject(self, module):
        self.type = self.getClass(module, self.data["Type"])
        self.type.loadProperties(self.data["Properties"])
        self.type.loadManifest(self.manifest)
    
    """
    Checks the conditions on the wrapper to make sure it is valid
    """
    def checkConditions(self):
        if "Conditions" in self.data:
            conditions = self.data["Conditions"]
            if "Platform" in conditions:
                platform = conditions["Platform"]
                if isinstance(platform, basestring):
                    platform = [platform]
                os = OperatingSystem().getOperatingSystem(self.os)
                if os not in platform:
                    g.feedback.log(LogLevels.DEBUG, "Unable to find OS %s in Platforms %s" % (os, platform))
                    return False
            if "Architecture" in conditions:
                architecture = conditions["Architecture"]
                if isinstance(architecture, basestring):
                    architecture = [architecture]
                arch = Architecture().getArchitecture(self.arch)
                if arch not in architecture:
                    g.feedback.log(LogLevels.DEBUG, "Unable to find architecture %s in Architectures %s" % (arch, architecture))
                    return False
        return True
    
    """
    Constructor which gets the data, OS and architecture
    """
    def __init__(self, manifest, data, os, arch):
        self.manifest = manifest
        self.data = data
        self.os = os
        self.arch = arch
        self.load()