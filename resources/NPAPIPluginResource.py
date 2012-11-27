from FileResource import FileResource
from env.enums import OperatingSystem
import os
import g

class NPAPIPluginResource(FileResource):
    
    def getType(self):
        return "Jinn::Resource::NPAPIPlugin"
    
    def doInstall(self):
        global jinn
        
        # Download the file
        super(NPAPIPluginResource, self).doInstall()
        
        if self.os is OperatingSystem.LIN:
            targetdir = self.getHomeDirectory() + self.sep() + ".mozilla" + self.sep() + "plugins"
            self.makeDirectory(targetdir)
            target = targetdir + self.sep() + self.getFileNameFromPath(self.filename)
            f = g.jinn.getInstallTargetDirectory() + self.sep() + self.filename
            try:
                os.symlink(f, target)
                return True
            except:
                return False