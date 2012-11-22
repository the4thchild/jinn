from exceptions import *
from activity.ActivityWrapper import ActivityWrapper

"""
Action object which represents a basic action wrapper
"""
class ActionWrapper(ActivityWrapper):

    # Whether action is on by default
    default = False
    
    """
    Load our data from the object into the class
    """
    def load(self):
        try:
            super(ActionWrapper, self).load()
            self.type = self.getClass("actions", self.data["Type"])
            self.type.loadProperties(self.data["Properties"])
            if "Default" in self.data:
                self.default = self.data["Default"]
        except KeyError as e:
            raise ActionDataMissingException("Unable to find the required key %s" % e)