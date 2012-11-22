import sys
import inspect
from exceptions import *

"""
General code which applies to all activity wrappers
"""
class ActivityWrapper(object):
    
    # The data for the activity (from config file)
    data = None
    
    # The type of this activity
    type = None
    
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
    
    def load(self):
        if "Description" in self.data:
                self.description = self.data["Description"]
        self.properties = self.data["Properties"]
        if "Conditions" in self.data:
            self.conditions = self.data["Conditions"]
    
    """
    Constructor which gets the data, OS and architecture
    """
    def __init__(self, data, os, arch):
        self.data = data
        self.os = os
        self.arch = arch
        self.load()