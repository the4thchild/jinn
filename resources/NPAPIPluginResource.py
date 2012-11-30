from FileResource import FileResource
from env.enums import OperatingSystem
import os
import g
from feedback.LogLevels import LogLevels

class NPAPIPluginResource(FileResource):
    
    def getType(self):
        return "Jinn::Resource::NPAPIPlugin"
    

    def getMyFileName(self):
        return self.getFileNameFromPath(self.getFilename(self.getProperty("Source"), self.getProperty("Path"), self.getProperty("Name", False)))

    def getLinuxTargets(self):
        targetdir = self.getHomeDirectory() + self.sep() + ".mozilla" + self.sep() + "plugins"
        target = targetdir + self.sep() + self.getMyFileName()
        return (targetdir, target)
    
    def getLinuxTargetConfigFile(self):
        return g.jinn.getInstallTargetDirectory() + self.sep() + self.filename

    def doInstall(self):
        # Download the file
        super(NPAPIPluginResource, self).doInstall()
        
        if self.os is OperatingSystem.LIN:
            targetdir,target = self.getLinuxTargets()
            self.makeDirectory(targetdir)
            f = self.getLinuxTargetConfigFile()
            try:
                self.delete(f)
                os.symlink(f, target)
                return True
            except:
                return False
        elif self.os is OperatingSystem.WIN:
            cmd = "regsvr32 /s " + self.getProperty("Path") + self.sep() + self.getMyFileName()
            g.feedback.log(LogLevels.DEBUG, "Registering with command %s" % cmd)
            res = os.system(cmd)
            if res < 1:
                return True
            else:
                g.feedback.log(LogLevels.ERROR, "Calling regsvr failed, command was %s, result was %s" % (cmd, str(res)))
                return False
        elif self.os is OperatingSystem.OSX:
            # For now
            return True
            
    def doUninstall(self):
        if self.os is OperatingSystem.LIN:
            targetdir,target = self.getLinuxTargets()
            if not self.delete(target):
                return False
            return True
        elif self.os is OperatingSystem.WIN:
            target = self.getProperty("Path") + self.sep() + self.getMyFileName()
            cmd = "regsvr32 /s -u " + target
            g.feedback.log(LogLevels.DEBUG, "Unregistering with command %s" % cmd)
            res = os.system(cmd)
            if res > 0:
                g.feedback.log(LogLevels.ERROR, "Calling regsvr failed, command was %s, result was %s" % (cmd, str(res)))
                return False
            if not self.delete(target):
                return False
            return True
        elif self.os is OperatingSystem.OSX:
            # For now
            return True