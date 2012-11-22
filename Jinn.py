import sys
import os
import options
import g

from feedback import FeedbackMechanisms
from manifest.Manifest import Manifest
from feedback.ConsoleFeedback import ConsoleFeedback
from feedback.UIFeedback import UIFeedback
from feedback.FeedbackBase import FeedbackBase
from feedback.LogLevels import LogLevels

class Jinn(object):
    
    # The current manifest, as loaded from the filesystem
    current_manifest = None
    
    # The new manifest, as loaded from the remote URL
    new_manifest = None
    
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
        
        manifest = Manifest(options.manifest, options.manifest_is_url)
        g.feedback.log(LogLevels.DEBUG, "Default action")
        return 0
    
    """
    Runs a specific action within the jinn
    """
    def runAction(self, action):
        if not self.isInstalled():
            g.feedback.log(LogLevels.ERROR, "Cannot run action %s, this jinn is not installed" % action)
            g.feedback.userMessage("Installation failed (2) - please contact distributor")
            return 1
            
        g.feedback.log(LogLevels.DEBUG, "Run action %s" % action)
        return 0
    
    """
    Runs an installation of this jinn
    """
    def doInstall(self):
        if self.isInstalled():
            g.feedback.log(LogLevels.ERROR, "This jinn is already insalled")
            g.feedback.userMessage("Installation failed (3) - please contact distributor")
            return 1
        
        g.feedback.log(LogLevels.DEBUG, "Installing")
        return 0
    
    """
    Runs uninstallation
    """
    def doUninstall(self):
        if not self.isInstalled():
            g.feedback.log(LogLevels.ERROR, "This jinn is not installed, so cannot be uninstalled")
            g.feedback.userMessage("Installation failed (4) - please contact distributor")
            return 1

        g.feedback.log(LogLevels.DEBUG, "Uninstalling")
        return 1
    
    """
    Check whether or not this jinn is currently installed
    """
    def isInstalled(self):
        return os.path.isdir(".jinn")
    
    """
    Output the help content
    """
    def doHelp(self):
        g.feedback.userMessage("""
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
A Java installer
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
        """)
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
        elif sys.argv[1] == "-action":
            if len(sys.argv) < 3:
                g.feedback.userMessage("For -action, you must specify an action - try -help")
                return 1
            return self.runAction(sys.argv[2])
    
    """
    Initialises the Jinn class, which handles all of the application lifecycle
    """
    def __init__(self):
        # Setup feedback mechanism
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
    jinn = Jinn()
    return jinn.do()

if __name__ == '__main__':
    status = main()
    g.feedback.userMessage("Jinn exiting with code %s" % str(status))
    sys.exit(status)