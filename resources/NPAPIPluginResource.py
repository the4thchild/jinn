from FileResource import FileResource
from env.enums import OperatingSystem
import os
import g

class NPAPIPluginResource(FileResource):
    
    def getType(self):
        return "Jinn::Resource::NPAPIPlugin"
    
    def getLinuxTargets(self):
        targetdir = self.getHomeDirectory() + self.sep() + ".mozilla" + self.sep() + "plugins"
        target = targetdir + self.sep() + self.getFileNameFromPath(self.filename)
        return (targetdir, target)
    
    def getLinuxTargetConfigFile(self):
        return g.jinn.getInstallTargetDirectory() + self.sep() + self.filename

    def doInstall(self):
        global jinn
        
        # Download the file
        super(NPAPIPluginResource, self).doInstall()
        
        if self.os is OperatingSystem.LIN:
            targetdir,target = self.getLinuxTargets()
            self.makeDirectory(targetdir)
            f = self.getLinuxTargetConfigFile()
            try:
                os.symlink(f, target)
                return True
            except:
                return False
            
    def doUninstall(self):
        if self.os is OperatingSystem.LIN:
            targetdir,target = self.getLinuxTargets()
            if not self.delete(target):
                return False
            return True