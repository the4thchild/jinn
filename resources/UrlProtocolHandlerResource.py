from resource.ResourceBase import ResourceBase
from env.enums import OperatingSystem
import g

class UrlProtocolHandlerResource(ResourceBase):
    
    def getType(self):
        return "Jinn::Resource::UrlProtocolHandler"
    
    def getLinuxFileDirectory(self):
        return self.getHomeDirectory() + self.sep() + ".local" + self.sep() + "share" + self.sep() + "applications"
    
    def getLinuxFileName(self, protocol):
        return protocol + ".desktop"
    
    def getLinuxConfigString(self, protocol):
        return "x-scheme-handler/%s=%s.desktop" % (protocol,protocol)
    
    def getLinuxConfigFile(self):
        return self.getLinuxFileDirectory() + self.sep() + "mimeapps.list"
    
    def getLinuxFileContents(self, terminal, executable, name, description, protocol):
        return """[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Terminal=%s
Exec=%s "%sU"
Name=%s
Comment=%s
Categories=Application;Network;
MimeType=x-scheme-handler/%s
""" % (str(terminal), executable, "%", name, description, protocol)
    
    def doInstall(self):
        # Load up the variables
        protocol = self.getProperty("Protocol")
        if "Terminal" in self.properties:
            terminal = self.getProperty("Terminal")
        else:
            terminal = False
        if "Action" in self.properties:
            action = self.getProperty("Action")
        else:
            action = None
            
        name = g.jinn.manifest.jinn.name
        description = g.jinn.manifest.description
        executable = g.jinn.getInstallTargetFile()
        if g.jinn.isDevMode():
            executable = "python " + self.getCurrentFile()
        if action is not None:
            executable = executable + " -action " + action["Ref"]
        
        if self.os is OperatingSystem.LIN:
            a = self.saveToFile(self.getLinuxFileDirectory() + self.sep() + self.getLinuxFileName(protocol), self.getLinuxFileContents(terminal, executable, name, description, protocol))
            b = self.appendToFile(self.getLinuxConfigFile(), self.getLinuxConfigString(protocol))
            return a and b
        
    def doUninstall(self):
        protocol = self.getProperty("Protocol")
        
        if self.os is OperatingSystem.LIN:
            if not self.delete(self.getLinuxFileDirectory() + self.sep() + self.getLinuxFileName(protocol)):
                return False
            if not self.removeFromFile(self.getLinuxConfigFile(), self.getLinuxConfigString(protocol)):
                return False
            return True