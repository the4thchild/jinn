"""
A pretend enum for operating system
"""
class OperatingSystem(object):
    WIN = 1
    OSX = 2
    LIN = 3
    
    def getOperatingSystem(self, os):
        if os == self.WIN:
            return "WIN"
        elif os == self.OSX:
            return "OSX"
        elif os == self.LIN:
            return "LIN"
    
"""
A pretend enum for system architecture
"""
class Architecture(object):
    x32 = 2
    x64 = 4
    
    def getArchitecture(self, arch):
        if arch == self.x32:
            return "x32"
        elif arch == self.x64:
            return "x64"
    
"""
A pretend enum for os / architecture combo
"""
class Environment(object):
    WINx32 = OperatingSystem.WIN * Architecture.x32
    WINx64 = OperatingSystem.WIN * Architecture.x64
    OSXx32 = OperatingSystem.OSX * Architecture.x32
    OSXx64 = OperatingSystem.OSX * Architecture.x64
    LINx32 = OperatingSystem.LIN * Architecture.x32
    LINx64 = OperatingSystem.LIN * Architecture.x64