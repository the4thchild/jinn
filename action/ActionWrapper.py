from exceptions import *
from activity.ActivityWrapper import ActivityWrapper

"""
Action object which represents a basic action wrapper
"""
class ActionWrapper(ActivityWrapper):

    def __init__(self, id, manifest, data, os, arch):
        self.default = False
        
        super(ActionWrapper, self).__init__(id, manifest, data, os, arch)

    """
    Load our data from the object into the class
    """
    def load(self):
        try:
            super(ActionWrapper, self).load()
            super(ActionWrapper, self).loadPropertiesObject("actions")
            if "Default" in self.data:
                self.default = self.data["Default"]
        except KeyError as e:
            raise ActionDataMissingException("Unable to find the required key %s" % e)
        
    """
    Run this action
    """
    def run(self):
        return self.type.run()