import sys
import options
import g
import os
import copy
import platform
# Redundant import just for pyinstaller
import encodings

from feedback import FeedbackMechanisms
from manifest.Manifest import Manifest
from feedback.ConsoleFeedback import ConsoleFeedback
from feedback.UIFeedback import UIFeedback
from feedback.FeedbackBase import FeedbackBase
from feedback.LogLevels import LogLevels
from helpers.FileSystemHelper import FileSystemHelper
from env.enums import OperatingSystem, Architecture

class Jinn(FileSystemHelper):
    
    # Header for messages
    header = """
    .---.                           
    |   |                           
    '---'.--.   _..._      _..._    
    .---.|__| .'     '.  .'     '.  
    |   |.--..   .-.   ..   .-.   . 
    |   ||  ||  '   '  ||  '   '  | 
    |   ||  ||  |   |  ||  |   |  | 
    |   ||  ||  |   |  ||  |   |  | 
    |   ||  ||  |   |  ||  |   |  | 
    |   ||__||  |   |  ||  |   |  | 
 __.'   '    |  |   |  ||  |   |  | 
|      '     |  |   |  ||  |   |  | 
|____.'      '--'   '--''--'   '--' 
A Java installer"""

    def __init__(self):
        self.new_manifest = None
        self.manifest = None
        self.args = ""
        
        # Setup feedback mechanism
        global feedback
        if (options.interface == FeedbackMechanisms.CMD):
            g.feedback = ConsoleFeedback()
        elif (options.interface == FeedbackMechanisms.UI):
            g.feedback = UIFeedback()
        else:
            # Not specified, need something to stop errors, so us this
            g.feedback = FeedbackBase()
            
        self.os = self.getOperatingSystem()
        self.arch = self.getArchitecture()
            
        g.feedback.log(LogLevels.DEBUG, "Started up. OS: %s; Architecture: %s" % (OperatingSystem().getOperatingSystem(self.os), Architecture().getArchitecture(self.arch)))
    
    """
    Gets the current OS
    """
    def getOperatingSystem(self):
        p = platform.system()
        if p == "Windows":
            return OperatingSystem.WIN
        elif p == "Darwin":
            return OperatingSystem.OSX
        elif p == "Linux":
            return OperatingSystem.LIN
        else:
            g.feedback.log(LogLevels.ERROR, "Unable to work with operating system %s" % p)
            raise OperatingSystemNotFoundException(p)
    
    """
    Gets the current architecture
    """
    def getArchitecture(self):
        if self.os is OperatingSystem.WIN:
            g.feedback.log(LogLevels.DEBUG, "Getting architecture, we are windows, so asking the registry")
            return self.getArchitectureWindows()
        else:
            g.feedback.log(LogLevels.DEBUG, "Working out if we are running 32 or 64 bit")
            if(sys.maxsize > 2**32):
                g.feedback.log(LogLevels.DEBUG, "Decided 64 bit")
                return Architecture.x64
            else:
                g.feedback.log(LogLevels.DEBUG, "Decided 32 bit")
                return Architecture.x32
    
    """
    Windows special case for getting architecture
    """
    def getArchitectureWindows(self):
        from _winreg import *
        softwarekey = OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE")
        microsoftkey = OpenKey(softwarekey, "Microsoft")        
        windowskey = OpenKey(microsoftkey, "Windows NT")
        versionkey = OpenKey(windowskey, "CurrentVersion")
        value = QueryValueEx(versionkey, "BuildLabEx")[0]
        CloseKey(versionkey)
        CloseKey(windowskey)
        CloseKey(microsoftkey)
        CloseKey(softwarekey)
        if "amd64" in value:
            g.feedback.log(LogLevels.DEBUG, "From value %s, decided we are 64 bit" % value)
            return Architecture.x64
        else:
            g.feedback.log(LogLevels.DEBUG, "From value %s, decided we are 32 bit" % value)
            return Architecture.x32
    
    """
    Loads the manifest file
    """
    def loadManifest(self):
                
        g.feedback.log(LogLevels.DEBUG, "Loading new manifest from %s" % options.manifest)
        self.new_manifest = Manifest(self.os, self.arch, options.manifest, options.manifest_is_url)
        
        if self.isInstalled():
            manifest_file = ".jinn" + self.sep() + "current_manifest.json"
            g.feedback.log(LogLevels.DEBUG, "Loading manifest from %s" % manifest_file)
            self.manifest = Manifest(self.os, self.arch, manifest_file, False, True)
        else:
            g.feedback.log(LogLevels.DEBUG, "Loading manifest from new manifest, as not installed")
            self.manifest = self.new_manifest
    
    """
    A helper which sets up the system before a run
    """
    def setupSystem(self):
        
        g.feedback.log(LogLevels.DEBUG, "Setting up the system")
        
        # Make sure we are installed
        if not self.isInstalled():
            g.feedback.log(LogLevels.DEBUG, "We aren't installed, so installing")
            status = self.doInstall()
            if status != 0:
                g.feedback.log(LogLevels.ERROR, "Tried installing but failed horribly")
                g.feedback.userMessage("Installation failed (1) - please contact distributor")
                return status
            g.feedback.log(LogLevels.DEBUG, "Installation succeeded")
        else:
            self.loadManifest()
            
        return self.doUpdate()
    
    """
    Runs the default action in the jinn
    """
    def runDefaultAction(self):
        g.feedback.log(LogLevels.DEBUG, "Running default action")
        
        self.setupSystem()
        
        g.feedback.log(LogLevels.DEBUG, "Default action execution commencing")
        try:
            self.manifest.runDefaultAction(self.args)
            g.feedback.log(LogLevels.DEBUG, "Run default action executed successfully")
            return 0
        except Exception as e:
            g.feedback.log(LogLevels.ERROR, "Running default action threw exception %s" % e)
            return 1
    
    """
    Runs a specific action within the jinn
    """
    def runAction(self, action):
        
        g.feedback.log(LogLevels.DEBUG, "Running %s action" % action)
        
        self.setupSystem()
            
        g.feedback.log(LogLevels.DEBUG, "Run action %s" % action)
        try:
            self.manifest.runAction(action, self.args)
            g.feedback.log(LogLevels.DEBUG, "Running action %s successfully completed" % action)
            return 0
        except Exception as e:
            g.feedback.log(LogLevels.ERROR, "Running action %s threw exception %s" % (action, e))
            return 1
    
    """
    Are we in dev mode?
    """
    def isDevMode(self):
        isDev = options.version is "DEV"
        g.feedback.log(LogLevels.DEBUG, "Dev mode? %s" % str(isDev))
        return isDev

    """
    Checks the manifests for updates
    """
    def doUpdate(self):
        
        g.feedback.log(LogLevels.DEBUG, "Starting update procedure")
        
        # No update if the version number is the same
        if self.manifest.jinn.version == self.new_manifest.jinn.version:
            g.feedback.log(LogLevels.DEBUG, "New and current manifest versions are %s and %s, so skipping update as they are identical" % (self.manifest.jinn.version, self.new_manifest.jinn.version))
            return True
        
        g.feedback.log(LogLevels.DEBUG, "Setting installation status across manifests")
        # Initially, set the resources that are installed on the new manifest already
        if not self.new_manifest.setInstallStatus(self.manifest.resources):
            g.feedback.log(LogLevels.ERROR, "Failed to set install status")
            return False
        
        g.feedback.log(LogLevels.DEBUG, "Installing new resources")
        # First, install resources that are new
        if not self.new_manifest.installNewResources(self.manifest.resources):
            g.feedback.log(LogLevels.ERROR, "Failed to install new resources")
            return False
        
        g.feedback.log(LogLevels.DEBUG, "Uninstalling removed resources")
        # Second, uninstall resources that are gone
        if not self.new_manifest.uninstallRemovedResources(self.manifest.resources):
            g.feedback.log(LogLevels.ERROR, "Removing resources failed")
            return False
        
        g.feedback.log(LogLevels.DEBUG, "Updating changed resources")
        # Third, update resources that are new version
        if not self.new_manifest.updateResources(self.manifest.resources):
            g.feedback.log(LogLevels.ERROR, "Updating changed resources failed")
            return False
        
        g.feedback.log(LogLevels.DEBUG, "Saving manifest")
        # Finally, transition the manifest over to the new one
        self.manifest = self.new_manifest
        if not self.manifest.save():
            g.feedback.log(LogLevels.ERROR, "Unable to save updated manifest")
            return False
        
        # Done!
        g.feedback.log(LogLevels.DEBUG, "Update complete")
        return True
            

    """
    Copy this executable to the target directory, then run it
    """
    def doCopy(self):
        g.feedback.log(LogLevels.DEBUG, "We are not in the correct directory, so installing to the correct location")
        
        targetFile = self.getInstallTargetFile()
        g.feedback.log(LogLevels.DEBUG, "Target file is %s" % targetFile)
        d = self.getInstallTargetDirectory()
        g.feedback.log(LogLevels.DEBUG, "Target directory is %s" % d)
        if not self.exists(targetFile):
            # Make the jinn install directory
            if not self.makeDirectory(d):
                g.feedback.log(LogLevels.ERROR, "Unable to make directory %s to install to" % d)
                return 1
            
            # Copy this binary into it
            frm = self.getCurrentFile()
            to = targetFile
            g.feedback.log(LogLevels.DEBUG, "Copying from %s to %s" % (frm, to))
            if not self.copyFile(frm, to):
                g.feedback.log(LogLevels.ERROR, "Unable to copy %s to %s" % (frm,to))
                return 1
        
        # Change into that directory
        g.feedback.log(LogLevels.DEBUG, "Changing to %s" % d)
        if not self.changeDirectory(d):
            g.feedback.log(LogLevels.ERROR, "Unable to change to the InstallTargetDirectory %s" % d)
            return 1
        
        # Run the new executable
        g.feedback.log(LogLevels.DEBUG, "Code copied to %s, executing" % targetFile)
        cmd = self.getExecutableName() + " -install"
        if self.os == OperatingSystem.LIN or self.os == OperatingSystem.OSX:
            cmd = "./" + cmd
        g.feedback.log(LogLevels.DEBUG, "Run command: %s" % cmd)
        os.system(cmd)
        return 0

    """
    Runs an installation of this jinn
    """
    def doInstall(self):
        
        g.feedback.log(LogLevels.DEBUG, "Beginning installation")
        
        # We need the manifest first of all
        self.loadManifest()
        
        # Hard code here to not happen for dev
        correctDir = self.isCorrectDirectory()
        g.feedback.log(LogLevels.DEBUG, "Are we in correct directory? %s" % str(correctDir))
        if not correctDir and not self.isDevMode():
            return self.doCopy()
    
        # Make sure we are in the right directory
        installDir = self.getInstallTargetDirectory()
        g.feedback.log(LogLevels.DEBUG, "Target install dir is %s" % installDir)
        if not self.changeDirectory(installDir) and not self.isDevMode():
            g.feedback.log(LogLevels.ERROR, "Unable to change to where we thought we were installed, %s" % installDir)
            return 1
        
        if self.isInstalled():
            g.feedback.log(LogLevels.ERROR, "This jinn is already installed")
            g.feedback.userMessage("Installation failed (3) - please contact distributor")
            return 1
        
        g.feedback.log(LogLevels.DEBUG, "Installing")
        
        if not self.makeDirectory(".jinn"):
            g.feedback.log(LogLevels.ERROR, "Unable to make .jinn directory")
            return 1
        
        if not self.manifest.save():
            g.feedback.log(LogLevels.ERROR, "Unable to save the manifest")
            return 1
        
        try:
            if self.manifest.installResources():
                g.feedback.log(LogLevels.DEBUG, "Install resources succeeded")
                return 0
            else:
                g.feedback.log(LogLevels.ERROR, "Install resources failed")
                return 1
        except Exception as e:
            g.feedback.log(LogLevels.ERROR, "Unable to install resources: %s" % e)
            return 1
    
    """
    Runs uninstallation
    """
    def doUninstall(self):
        
        g.feedback.log(LogLevels.DEBUG, "Doing uninstallation")
        
        if not self.isInstalled():
            g.feedback.log(LogLevels.ERROR, "This jinn is not installed, so cannot be uninstalled")
            g.feedback.userMessage("Uninstallation failed (4) - please contact distributor")
            return 1

        g.feedback.log(LogLevels.DEBUG, "Uninstalling")
        
        self.loadManifest()
        
        try:
            if self.manifest.uninstallResources():
                if self.delete(".jinn"):
                    g.feedback.userMessage("Uninstallation finished. To completely erase this application, please delete the directory %s" % self.getInstallTargetDirectory())
                    return 0
                else:
                    g.feedback.log(LogLevels.ERROR, "Failed to delete .jinn directory, will think its still installed")
                    return 1
            else:
                g.feedback.log(LogLevels.ERROR, "Uninstallation failed")
                return 1
        except Exception as e:
            g.feedback.log(LogLevels.ERROR, "Unable to uninstall: %s" % e)
            return 1
    
    """
    Returns the install target directory
    """
    def getInstallTargetDirectory(self):
        if self.isDevMode():
            return self.getCurrentDirectory()
        else:
            return self.getHomeDirectory() + self.getDirectorySeparator() + self.manifest.jinn.name

    """
    Get the name of the executabl
    """
    def getExecutableName(self):
        if self.os == OperatingSystem.WIN:
            return self.manifest.jinn.name + ".jinn.exe"
        else:
            return self.manifest.jinn.name + ".jinn"

    """
    Get the file we wish to install to
    """
    def getInstallTargetFile(self):
        return self.getInstallTargetDirectory() + self.getDirectorySeparator() + self.getExecutableName()

    """
    Check whether or not we are running from the right place
    """
    def isCorrectDirectory(self):
        currentdir = self.getCurrentDirectory()
        targetdir = self.getInstallTargetDirectory()
        
        g.feedback.log(LogLevels.DEBUG, "Current directory: %s" % currentdir)
        g.feedback.log(LogLevels.DEBUG, "Target dir: %s" % targetdir)
        
        return targetdir == currentdir
    
    """
    Take the sys args and turn them into a string stored on the object
    for later use. Offset is how many to skip off the front.
    Automatically skips the first one, the current script
    """
    def processArgs(self, offset = 0):
        args = copy.copy(sys.argv)
        args.pop(0)
        i = 0
        while i < offset:
            args.pop(0)
            i += 1
        self.args = " ".join(map(str, args))
        g.feedback.log(LogLevels.DEBUG, "System args: %s" % self.args)
    
    """
    Check whether or not this jinn is currently installed
    """
    def isInstalled(self):
        return self.directoryExists(".jinn")
    
    """
    Output the version information
    """
    def doVersion(self):
        g.feedback.userMessage("""
%s
Version: %s
""" % (self.header, options.version))
        return 0
    
    """
    Output the help content
    """
    def doHelp(self):
        g.feedback.userMessage("""
%s
Created by import.io
        
Options:
    ./jinn
        Run the jinn with the default action
    ./jinn -install
        Run the jinn installation
    ./jinn -uninstall
        Uninstall the jinn
    ./jinn -help
        Display this helpful help dialog
    ./jinn -action (actionname)
        Run the jinn action specified by (actionname)
    ./jinn -version
        Print the version string
        """ % self.header)
        return 0
    
    """
    Runs the jinn feature we need to perform
    """
    def do(self):
        
        # Change to the current run directory
        self.changeDirectory(self.getPathFromFilePath(sys.argv[0]))
        
        # Analyse the sys args to figure out what to do
        if len(sys.argv) < 2:
            # No extra args, if we are installed we want to run the default action.
            # Otherwise this is the first run from download, so do install
            if self.isInstalled():
                return self.runDefaultAction()
            else:
                return self.doInstall()
        elif sys.argv[1] == "-install":
            return self.doInstall()
        elif sys.argv[1] == "-uninstall":
            return self.doUninstall()
        elif sys.argv[1] == "-help":
            return self.doHelp()
        elif sys.argv[1] == "-version":
            return self.doVersion()
        elif sys.argv[1] == "-action":
            if len(sys.argv) < 3:
                g.feedback.userMessage("For -action, you must specify an action - try -help")
                return 1
            self.processArgs(2)
            return self.runAction(sys.argv[2])
        else:
            # There are some args, we don't recognise the first, so must want to run default action with some args
            self.processArgs()
            return self.runDefaultAction()


class OperatingSystemNotFoundException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

"""
Main function that is run when the code is started from this file
"""
def main():
    g.jinn = Jinn()
    return g.jinn.do()

if __name__ == '__main__':
    status = main()
    g.feedback.userMessage("Jinn exiting with code %s" % str(status))
    sys.exit(status)