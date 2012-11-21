import sys
import os
import options

from manifest.Manifest import Manifest

class Jinn:
    
    # The current manifest, as loaded from the filesystem
    current_manifest = None
    
    # The new manifest, as loaded from the remote URL
    new_manifest = None
    
    """
    Runs the default action in the jinn
    """
    def runDefaultAction(self):
        if not self.isInstalled():
            print "Cannot run default action, this jinn is not installed"
            return 1
        
        print "Default action"
        return 0
    
    """
    Runs a specific action within the jinn
    """
    def runAction(self, action):
        if not self.isInstalled():
            print "Cannot run action %s, this jinn is not installed" % action
            return 1
            
        print "Run action %s" % action
        return 0
    
    """
    Runs an installation of this jinn
    """
    def doInstall(self):
        if self.isInstalled():
            print "This jinn is already installed"
            return 1
        
        print "Installing"
        return 0
    
    """
    Runs uninstallation
    """
    def doUninstall(self):
        if not self.isInstalled():
            print "This jinn is not installed, so cannot be uninstalled"
            return 1
        
        # TODO: Uninstallation
        print "Uninstall not implemented yet"
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
        print """
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
        """
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
                print "For -action, you must specify an action - try -help"
                return 1
            return self.runAction(sys.argv[2])
    
    """
    Initialises the Jinn class, which handles all of the application lifecycle
    """
    def __init__(self):
        #manifest = Manifest(options.manifest, options.manifest_is_url)
        pass

"""
Main function that is run when the code is started from this file
"""
def main():
    jinn = Jinn()
    return jinn.do()

if __name__ == '__main__':
    status = main()
    print "Jinn exiting with code %s" % str(status)
    sys.exit(status)