import sys
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
        print "Default action"
        return 0
    
    """
    Runs a specific action within the jinn
    """
    def runAction(self, action):
        print "Run action %s" % action
        return 0
    
    """
    Runs an installation of this jinn
    """
    def doInstall(self):
        print "Install"
        return 0
    
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
        Run with the default action
    ./jinn -install
        Run the installation
    ./jinn -help
        Display this help dialog
    ./jinn -action (actionname)
        Run the action specified by (actionname)
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
    sys.exit(status)