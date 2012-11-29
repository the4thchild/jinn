import sys
import options
import g
import os
import copy
# Redundant import just for pyinstaller
import encodings

from feedback import FeedbackMechanisms
from manifest.Manifest import Manifest
from feedback.ConsoleFeedback import ConsoleFeedback
from feedback.UIFeedback import UIFeedback
from feedback.FeedbackBase import FeedbackBase
from feedback.LogLevels import LogLevels
from helpers.FileSystemHelper import FileSystemHelper

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
    
    def loadManifest(self):
                
        g.feedback.log(LogLevels.DEBUG, "Loading new manifest from %s" % options.manifest)
        self.new_manifest = Manifest(options.manifest, options.manifest_is_url)
        
        if self.isInstalled():
            manifest_file = ".jinn" + self.sep() + "current_manifest.json"
            g.feedback.log(LogLevels.DEBUG, "Loading manifest from %s" % manifest_file)
            self.manifest = Manifest(manifest_file, False, True)
        else:
            g.feedback.log(LogLevels.DEBUG, "Loading manifest from new manifest, as not installed")
            self.manifest = self.new_manifest
    
    """
    A helper which sets up the system before a run
    """
    def setupSystem(self):
        # Make sure we are installed
        if not self.isInstalled():
            status = self.doInstall()
            if status != 0:
                g.feedback.log(LogLevels.ERROR, "Tried installing but failed horribly")
                g.feedback.userMessage("Installation failed (1) - please contact distributor")
                return status
        else:
            self.loadManifest()
            
        return self.doUpdate()
    
    """
    Runs the default action in the jinn
    """
    def runDefaultAction(self):
        self.setupSystem()
        
        g.feedback.log(LogLevels.DEBUG, "Default action")
        try:
            self.manifest.runDefaultAction(self.args)
            return 0
        except:
            return 1
    
    """
    Runs a specific action within the jinn
    """
    def runAction(self, action):
        self.setupSystem()
            
        g.feedback.log(LogLevels.DEBUG, "Run action %s" % action)
        try:
            self.manifest.runAction(action, self.args)
            return 0
        except:
            return 1
    
    """
    Are we in dev mode?
    """
    def isDevMode(self):
        return options.version is "DEV"

    """
    Checks the manifests for updates
    """
    def doUpdate(self):
        
        # No update if the version number is the same
        if self.manifest.jinn.version == self.new_manifest.jinn.version:
            g.feedback.log(LogLevels.DEBUG, "New and current manifest versions are %s and %s, so skipping update as they are identical" % (self.manifest.jinn.version, self.new_manifest.jinn.version))
            return True
        
        # Initially, set the resources that are installed on the new manifest already
        if not self.new_manifest.setInstallStatus(self.manifest.resources):
            return False
        
        # First, install resources that are new
        if not self.new_manifest.installNewResources(self.manifest.resources):
            return False
        
        # Second, uninstall resources that are gone
        if not self.new_manifest.uninstallRemovedResources(self.manifest.resources):
            return False
        
        # Third, update resources that are new version
        if not self.new_manifest.updateResources(self.manifest.resources):
            return False
        
        # Finally, transition the manifest over to the new one
        self.manifest = self.new_manifest
        if not self.manifest.save():
            return False
        
        # Done!
        return True
            

    """
    Copy this executable to the target directory, then run it
    """
    def doCopy(self):
        g.feedback.log(LogLevels.DEBUG, "We are not in the correct directory, so installing to the correct location")
        
        if not self.exists(self.getInstallTargetFile()):
            # Make the jinn install directory
            d = self.getInstallTargetDirectory()
            if not self.makeDirectory(d):
                g.feedback.log(LogLevels.ERROR, "Unable to make directory %s to install to" % d)
                return 1
            
            # Copy this binary into it
            frm = self.getCurrentFile()
            to = self.getInstallTargetFile()
            if not self.copyFile(frm, to):
                g.feedback.log(LogLevels.ERROR, "Unable to copy %s to %s" % (frm,to))
                return 1
        
        # Change into that directory
        if not self.changeDirectory(self.getInstallTargetDirectory()):
            g.feedback.log(LogLevels.ERROR, "Unable to change to the InstallTargetDirectory")
            return 1
        
        # Run the new executable
        g.feedback.log(LogLevels.DEBUG, "Code copied to %s, executing" % to)
        cmd = "./" + self.getExecutableName() + " -install"
        g.feedback.log(LogLevels.DEBUG, "Run command: %s" % cmd)
        os.system(cmd)
        return 0

    """
    Runs an installation of this jinn
    """
    def doInstall(self):
        # We need the manifest first of all
        self.loadManifest()
        
        # Hard code here to not happen for dev
        if not self.isCorrectDirectory() and not self.isDevMode():
            return self.doCopy()
    
        # Make sure we are in the right directory
        installDir = self.getInstallTargetDirectory()
        if not self.changeDirectory(installDir) and not self.isDevMode():
            g.feedback.log(LogLevels.ERROR, "Unable to change to where we thought we were installed, %s" % installDir)
            return 1
        
        if self.isInstalled():
            g.feedback.log(LogLevels.ERROR, "This jinn is already installed")
            g.feedback.userMessage("Installation failed (3) - please contact distributor")
            return 1
        
        g.feedback.log(LogLevels.DEBUG, "Installing")
        
        if not self.makeDirectory(".jinn"):
            return 1
        
        if not self.manifest.save():
            g.feedback.log(LogLevels.ERROR, "Unable to save the manifest")
            return 1
        
        try:
            if self.manifest.installResources():
                return 0
            else:
                return 1
        except Exception as e:
            g.feedback.log(LogLevels.ERROR, "Unable to install resources: %s" % e)
            return 1
    
    """
    Runs uninstallation
    """
    def doUninstall(self):
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
                    return 1
            else:
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
        # TODO: Platform dependency here
        return "builder.bin"

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
                self.doInstall()
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