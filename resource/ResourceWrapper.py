from exceptions import *
from activity.ActivityWrapper import ActivityWrapper

"""
Resource object which represents a basic resource wrapper
"""
class ResourceWrapper(ActivityWrapper):
    
    # Version of the resource
    version = None
    
    """
    Load our data from the object into the class
    """
    def load(self):
        try:
            self.type = self.getClass("resources", self.data["Type"])
            self.type.loadProperties(self.data["Properties"])
            if "Description" in self.data:
                self.description = self.data["Description"]
            self.properties = self.data["Properties"]
            if "Conditions" in self.data:
                self.conditions = self.data["Conditions"]
            self.version = self.data["Version"]
        except KeyError as e:
            raise ResourceDataMissingException("Unable to find the required key %s" % e)