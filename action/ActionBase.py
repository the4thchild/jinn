import g
from activity.ActivityBase import ActivityBase
from feedback.LogLevels import LogLevels

"""
A base class for Actions, providing interfaces they may wish to
implement
"""
class ActionBase(ActivityBase):
    
    """
    Command the action to run
    """
    def doRun(self):
        g.feedback.log(LogLevels.ERROR, "Action does not implement doRun")
        return 1
    
    