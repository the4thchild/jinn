"""
A pretend enum for operating system
"""
class OperatingSystem:
    WIN = 1
    OSX = 2
    LIN = 3
    
"""
A pretend enum for system architecture
"""
class Architecture:
    x32 = 2
    x64 = 4
    
"""
A pretend enum for os / architecture combo
"""
class Environment:
    WINx32 = OperatingSystem.WIN * Architecture.x32
    WINx64 = OperatingSystem.WIN * Architecture.x64
    OSXx32 = OperatingSystem.OSX * Architecture.x32
    OSXx64 = OperatingSystem.OSX * Architecture.x64
    LINx32 = OperatingSystem.LIN * Architecture.x32
    LINx64 = OperatingSystem.LIN * Architecture.x64