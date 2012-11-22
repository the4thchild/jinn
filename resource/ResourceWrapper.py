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
            super(ResourceWrapper, self).load()
            super(ResourceWrapper, self).loadPropertiesObject("resources")
            self.version = self.data["Version"]
        except KeyError as e:
            raise ResourceDataMissingException("Unable to find the required key %s" % e)
        
    """
    Install this resource
    """
    def doInstall(self):
        return self.type.doInstall()