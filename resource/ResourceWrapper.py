from exceptions import *
from activity.ActivityWrapper import ActivityWrapper
import g
from feedback.LogLevels import LogLevels

"""
Resource object which represents a basic resource wrapper
"""
class ResourceWrapper(ActivityWrapper):
    
    # Version of the resource
    version = None
    
    # Dependencies, if any
    depends = None
    
    # Whether or not we are installed
    isInstalled = False
    
    # Whether we are currently installing
    isInstalling = False
    
    """
    Load our data from the object into the class
    """
    def load(self):
        try:
            super(ResourceWrapper, self).load()
            super(ResourceWrapper, self).loadPropertiesObject("resources")
            self.version = self.data["Version"]
            if "Depends" in self.data:
                self.depends = self.data["Depends"]
        except KeyError as e:
            raise ResourceDataMissingException("Unable to find the required key %s" % e)
        
    """
    Install this resource
    """
    def doInstall(self):
        
        # Pre-check to make sure we haven't been installed already by dependencies
        if self.isInstalled:
            g.feedback.log(LogLevels.DEBUG, "Skipping installation of %s, it is already installed" % self.id)
            return True
        
        self.isInstalling = True;
        
        g.feedback.log(LogLevels.DEBUG, "Resolving dependencies of %s" % self.id)
        
        # Check dependencies
        if self.depends is not None:
            deps = self.depends
            if not type(deps) is list:
                deps = [deps]
            for dep in deps:
                try:
                    ref = dep["Ref"]
                except:
                    g.feedback.log(LogLevels.ERROR, "Unable to install %s, dependency must contain a Ref object" % self.id)
                    return False
                res = self.manifest.getResourceForId(ref)
                if res is None:
                    g.feedback.log(LogLevels.ERROR, "Unable to install %s, couldn't find dependency %s" % (self.id, ref))
                    return False
                if res.isInstalling:
                    g.feedback.log(LogLevels.ERROR, "Unable to install %s, dependency %s is already installing: circular dependency" % (self.id, ref))
                    return False
                if not res.isInstalled:
                    inst = res.doInstall()
                    if not inst:
                        g.feedback.log(LogLevels.ERROR, "Unable to install %s, dependency %s failed to install" % (self.id, ref))
                        return False
                else:
                    g.feedback.log(LogLevels.DEBUG, "Dependency %s of %s already installed" % (ref, self.id))
        
        g.feedback.log(LogLevels.DEBUG, "Beginning installation of %s" % self.id)
        
        res = self.type.doInstall()
        if res:
            g.feedback.log(LogLevels.DEBUG, "Installation of %s succeeded" % self.id)
            self.isInstalled = True
        else:
            g.feedback.log(LogLevels.DEBUG, "Installation of %s failed" % self.id)
            
        self.isInstalling = False
        return res