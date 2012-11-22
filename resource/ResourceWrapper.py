import sys
import inspect
from exceptions import *
from env.enums import OperatingSystem, Architecture

"""
Resource object which represents a basic resource wrapper
"""
class ResourceWrapper:
    
    # The data for the resource
    data = None
    
    # The type of this resource
    type = None
    
    # Description of the resource
    description = ""
    
    # Conditions of the resource
    conditions = None
    
    # Version of the resource
    version = None
    
    # The OS in use
    os = None
    
    # The architecture in use
    arch = None
    
    """
    Helper function which loads all the classes in the correct module,
    searches for ones with getType methods, and tries to find the
    one that matches the type given as input, returning an instance
    of it
    """
    def getClass(self, desiredType):
        clazzes = inspect.getmembers(sys.modules["resources"], inspect.isclass)
        for clazzdef in clazzes:
            clazz = clazzdef[1]
            obj = clazz(OperatingSystem.LIN, Architecture.x64)
            try:
                attr = getattr(obj, "getType")
                if callable(attr):
                    clazztype = obj.getType()
                    if clazztype == desiredType:
                        return obj
            except:
                pass
        raise ResourceNotFoundException("Unable to load resource for type %s" % desiredType)
    
    """
    Load our data from the object into the class
    """
    def load(self):
        try:
            self.type = self.getClass(self.data["Type"])
            self.type.loadProperties(self.data["Properties"])
            if "Description" in self.data:
                self.description = self.data["Description"]
            self.properties = self.data["Properties"]
            if "Conditions" in self.data:
                self.conditions = self.data["Conditions"]
            self.version = self.data["Version"]
        except KeyError as e:
            raise ResourceDataMissingException("Unable to find the required key %s" % e)
    
    def __init__(self, os, arch, data = None):
        if data != None:
            self.data = data
            self.os = os
            self.arch = arch
            self.load()