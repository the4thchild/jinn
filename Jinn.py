import sys
import options
import g
import os
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
    
    # The current manifest, as loaded from the filesystem
    current_manifest = None
    
    # The new manifest, as loaded from the remote URL
    new_manifest = None
    
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
    
    def loadManifest(self):
        g.feedback.log(LogLevels.DEBUG, "Loading manifest from %s" % options.manifest)
        self.manifest = Manifest(options.manifest, options.manifest_is_url)
        g.feedback.log(LogLevels.DEBUG, "Manifest is %s" % self.manifest)
    
    """
    Runs the default action in the jinn
    """
    def runDefaultAction(self):
        if not self.isInstalled():
            status = self.doInstall()
            if status != 0:
                g.feedback.log(LogLevels.ERROR, "Tried installing but failed horribly")
                g.feedback.userMessage("Installation failed (1) - please contact distributor")
                return status
        else:
            self.loadManifest()
        
        g.feedback.log(LogLevels.DEBUG, "Default action")
        try:
            self.manifest.runDefaultAction()
            return 0
        except:
            return 1
    
    """
    Runs a specific action within the jinn
    """
    def runAction(self, action):
        if not self.isInstalled():
            g.feedback.log(LogLevels.ERROR, "Cannot run action %s, this jinn is not installed" % action)
            g.feedback.userMessage("Installation failed (2) - please contact distributor")
            return 1
        else:
            self.loadManifest()
            
        g.feedback.log(LogLevels.DEBUG, "Run action %s" % action)
        try:
            self.manifest.runAction(action)
            return 0
        except:
            return 1
    
    """
    Are we in dev mode?
    """
    def isDevMode(self):
        return options.version is "DEV"

    """
    Runs an installation of this jinn
    """
    def doInstall(self):
        # We need the manifest first of all
        self.loadManifest()
        
        # Hard code here to not happen for dev
        if not self.isCorrectDirectory() and not self.isDevMode():
            g.feedback.log(LogLevels.DEBUG, "We are not in the correct directory, so changing to that")
            
            # Make the jinn install directory
            dir = self.getInstallTargetDirectory()
            if not self.makeDirectory(dir):
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
            os.system("./" + self.getExecutableName())
            return 0
    
        # Make sure we are in the right directory
        installDir = self.getInstallTargetDirectory()
        if not self.changeDirectory(installDir) and not self.isDevMode():
            g.feedback.log(LogLevels.ERROR, "Unable to change to where we thought we were installed, %s" % installDir)
            return 1
        
        if self.isInstalled():
            g.feedback.log(LogLevels.ERROR, "This jinn is already insalled")
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
        
        return targetdir is currentdir
    
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
        # Analyse the sys args to figure out what to do
        if len(sys.argv) < 2:
            # No extra args, want to run the default action
            return self.runDefaultAction()
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
            return self.runAction(sys.argv[2])
    
    """
    Initialises the Jinn class, which handles all of the application lifecycle
    """
    def __init__(self):
        #manifest = Manifest(options.manifest, options.manifest_is_url)
        
        # Setup feedback mechanism
        global feedback
        if (options.interface == FeedbackMechanisms.CMD):
            g.feedback = ConsoleFeedback()
        elif (options.interface == FeedbackMechanisms.UI):
            g.feedback = UIFeedback()
        else:
            # Not specified, need something to stop errors, so us this
            g.feedback = FeedbackBase()

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