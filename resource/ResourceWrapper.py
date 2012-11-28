from exceptions import *
from activity.ActivityWrapper import ActivityWrapper
import g
from feedback.LogLevels import LogLevels

"""
Resource object which represents a basic resource wrapper
"""
class ResourceWrapper(ActivityWrapper):
 
    def __init__(self, id, manifest, data, os, arch):
        self.isInstalled = False
        self.isInstalling = False
        self.depends = None
        self.version = None
        
        super(ResourceWrapper, self).__init__(id, manifest, data, os, arch)
    
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
        
    def setInstalled(self, installed):
        self.isInstalled = installed
        
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
    
    """
    Uninstall this resource
    """
    def doUninstall(self):
        
        # Pre-check to make sure we haven't been uninstalled already
        if not self.isInstalled:
            g.feedback.log(LogLevels.DEBUG, "Skipping uninstallation of %s, it is already uninstalled" % self.id)
            return True
        
        self.isInstalling = True
        
        g.feedback.log(LogLevels.DEBUG, "Resolving dependencies of %s" % self.id)
        
        # Check dependencies and uninstall those first
        for res in self.manifest.resources:
            if res.depends is not None:
                deps = res.depends
                if not type(deps) is list:
                    deps = [deps]
                for dep in deps:
                    try:
                        ref = dep["Ref"]
                    except:
                        g.feedback.log(LogLevels.ERROR, "Unable to uninstall %s, dependency must contain a Ref object" % self.id)
                        return False
                    if ref == self.id and res.isInstalled:
                        # Uninstall if it depends on us
                        uninst = res.doUninstall()
                        if not uninst:
                            g.feedback.log(LogLevels.ERROR, "Unable to uninstall %s, dependency %s failed to uninstall" % (self.id, res.name))
                            return False
        
        g.feedback.log(LogLevels.DEBUG, "Beginning uninstallation of %s" % self.id)
        
        res = self.type.doUninstall()
        if res:
            g.feedback.log(LogLevels.DEBUG, "Uninstallation of %s succeeded" % self.id)
            self.isInstalled = False
        else:
            g.feedback.log(LogLevels.DEBUG, "Uninstallation of %s failed" % self.id)
            
        self.isInstalling = False
        return res
    
    """
    Install all of the dependents, for example after an update
    Update process will first uninstall all of the dependents then the main resource
    Once the main resource has been reinstalled, the dependents can be reinstalled - 
    that is the process that occurs here
    Note this is a force-install, it ignores the installed flag
    """
    def installDependents(self):
        for res in self.manifest.resources:
            if res.depends is not None:
                deps = res.depends
                if not type(deps) is list:
                    deps = [deps]
                for dep in deps:
                    try:
                        ref = dep["Ref"]
                    except:
                        g.feedback.log(LogLevels.ERROR, "Unable to install %s, dependency must contain a Ref object" % self.id)
                        return False
                    if ref == self.id:
                        # Install if it is a dependent. Forcefully.
                        res.isInstalled = False
                        inst = res.doInstall()
                        if not inst:
                            g.feedback.log(LogLevels.ERROR, "Unable to install %s, dependency %s failed to install" % (self.id, res.name))
                            return False
        return True