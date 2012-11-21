from activity.ActivityBase import ActivityBase

"""
A base class for Actions, providing interfaces they may wish to
implement
"""
class ActionBase(ActivityBase):
    
    """
    Command the action to run
    """
    def doRun(self):
        print "Action does not implement doRun"
        return 1
    
    