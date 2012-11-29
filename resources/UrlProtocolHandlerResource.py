from resource.ResourceBase import ResourceBase
from env.enums import OperatingSystem
import g
from feedback.LogLevels import LogLevels
from copy import copy

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
        just_executable = copy(executable)
        if action is not None:
            a = ""
            if self.os is OperatingSystem.WIN:
                a = "\"" # If windows, each argument needs to be wrapped in quotes
            executable = a + executable + a + " " + a + "-action" + a + " " + a + action["Ref"] + a
        
        if self.os is OperatingSystem.LIN:
            a = self.saveToFile(self.getLinuxFileDirectory() + self.sep() + self.getLinuxFileName(protocol), self.getLinuxFileContents(terminal, executable, name, description, protocol))
            b = self.appendToFile(self.getLinuxConfigFile(), self.getLinuxConfigString(protocol))
            return a and b
        elif self.os is OperatingSystem.WIN:
            try:
                from _winreg import *
                softwarekey = OpenKey(HKEY_CURRENT_USER, "Software")
                classkey = OpenKey(softwarekey, "Classes")
                importkey = CreateKey(classkey, protocol)
                SetValue(classkey, protocol, REG_SZ, "URL:%s Handler" % protocol)
                SetValueEx(importkey, "URL Protocol", REG_SZ, 0, "")
                iconkey = CreateKey(importkey, "DefaultIcon")
                SetValue(importkey, "DefaultIcon", REG_SZ, "%s,1" % just_executable)
                shellkey =  CreateKey(importkey, "shell")
                openkey = CreateKey(shellkey, "open")
                commandkey = CreateKey(openkey, "command")
                SetValue(openkey, "command", REG_SZ, "%s \"%s1\"" % (executable, "%"))
                CloseKey(commandkey)
                CloseKey(openkey)
                CloseKey(shellkey)
                CloseKey(iconkey)
                CloseKey(importkey)
                CloseKey(classkey)
                CloseKey(softwarekey)
                return True
            except Exception as e:
                g.feedback.log(LogLevels.ERROR, "Exception playing with the registry, %s" % e)
                return False
        
    def doUninstall(self):
        protocol = self.getProperty("Protocol")
        
        if self.os is OperatingSystem.LIN:
            if not self.delete(self.getLinuxFileDirectory() + self.sep() + self.getLinuxFileName(protocol)):
                return False
            if not self.removeFromFile(self.getLinuxConfigFile(), self.getLinuxConfigString(protocol)):
                return False
            return True
        elif self.os is OperatingSystem.WIN:
            try:
                from _winreg import *
                softwarekey = OpenKey(HKEY_CURRENT_USER, "Software")
                classkey = OpenKey(softwarekey, "Classes")
                importkey = OpenKey(classkey, "importio")
                shellkey = OpenKey(importkey, "shell")
                openkey = OpenKey(shellkey, "open")
                DeleteKey(openkey, "command")
                CloseKey(openkey)
                DeleteKey(shellkey, "open")
                CloseKey(shellkey)
                DeleteKey(importkey, "shell")
                DeleteKey(importkey, "DefaultIcon")
                CloseKey(importkey)
                DeleteKey(HKEY_CLASSES_ROOT, "importio")
                CloseKey(classkey)
                CloseKey(softwarekey)
                return True
            except Exception as e:
                g.feedback.log(LogLevels.ERROR, "Exception playing with the registry, %s" % e)
                return False