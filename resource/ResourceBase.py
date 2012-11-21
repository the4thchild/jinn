from activity.ActivityBase import ActivityBase

"""
A base class for Resources, providing common
functions they may wish to implement
"""
class ResourceBase(ActivityBase):
    
    def doInstall(self):
        return 0
    
    def doUninstall(self):
        return 0