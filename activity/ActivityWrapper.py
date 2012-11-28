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
    
    """
    Constructor which gets the data, OS and architecture
    """
    def __init__(self, id, manifest, data, os, arch):
        self.type = None
        self.name = None
        self.description = ""
        self.conditions = None
        
        self.id = id
        self.manifest = manifest
        self.data = data
        self.os = os
        self.arch = arch
        
        self.load()
    
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
            try:
                obj = clazz(self.os, self.arch)
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
        # Check the conditions in the main object
        if "Conditions" in self.data:
            conditions = self.data["Conditions"]
            if "Platform" in conditions:
                platform = conditions["Platform"]
                if isinstance(platform, basestring):
                    platform = [platform]
                os = OperatingSystem().getOperatingSystem(self.os)
                if os not in platform:
                    g.feedback.log(LogLevels.DEBUG, "Unable to find OS %s in Platforms %s, so not working with activity %s" % (os, platform, self.name))
                    return False
            if "Architecture" in conditions:
                architecture = conditions["Architecture"]
                if isinstance(architecture, basestring):
                    architecture = [architecture]
                arch = Architecture().getArchitecture(self.arch)
                if arch not in architecture:
                    g.feedback.log(LogLevels.DEBUG, "Unable to find architecture %s in Architectures %s, so not working with activity %s" % (arch, architecture, self.name))
                    return False
        
        # Check the conditions are available in all properties which are platform specific too
        for name in self.properties:
            prop = self.properties[name]
            # See if property is a dict so must be a special object
            if type(prop) is dict:
                # Platform property type, so need to check we have the right one
                if "Platform" in prop:
                    plat = prop["Platform"]
                    # Do we have the OS
                    myos = OperatingSystem().getOperatingSystem(self.os)
                    if myos in plat:
                        opsys = plat[myos]
                        # Do we have the architecture too
                        myarch = Architecture().getArchitecture(self.arch)
                        if myarch in opsys:
                            # If we have the platform and architecture, we are good to continue
                            continue
                    if "Default" in plat:
                        # If we have a default we are good to continue
                        continue
                    g.feedback.log(LogLevels.DEBUG, "OS/architecture combo %s / %s is not available in activity %s, property %s, so not processing this activity" % (OperatingSystem().getOperatingSystem(self.os), Architecture().getArchitecture(self.arch), self.name, name))
                    return False
        
        return True
    
    """
    Return the ID of the activity
    """
    def getId(self):
        return self.id