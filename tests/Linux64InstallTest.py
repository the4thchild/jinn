'''
Created on 30 Nov 2012

@author: dev
'''
import unittest
import g
import platform
import Jinn
import os

from env.enums import OperatingSystem, Architecture
from feedback.LogLevels import LogLevels
from feedback.ConsoleFeedback import ConsoleFeedback
from helpers import FileSystemHelper

class Test(unittest.TestCase):


    def setUp(self):
        
        self.j = Jinn()
        
        self.new_manifest = None
        self.manifest = None
        self.args = ""
        
        # Setup feedback mechanism
        global feedback
        g.feedback = ConsoleFeedback()
        
        self.os = self.getOperatingSystem()
        self.arch = self.getArchitecture()
            
        g.feedback.log(LogLevels.DEBUG, "Started up. OS: %s; Architecture: %s" % (OperatingSystem().getOperatingSystem(self.os), Architecture().getArchitecture(self.arch)))
        
        #save a copy of the original options file
        self.old_options = "manifest=\"manifests/import_manifest.json\"\n# TODO: Get rid of this\nmanifest_is_url = False\ninterface = \"cmd\"\nversion = \"DEV\""
        
        #out new options file with the test manifest
        testoptions = "manifest=\"manifests/updates/archive/add/1.json\"\n# TODO: Get rid of this\nmanifest_is_url = False\ninterface = \"cmd\"\nversion = \"DEV\""
        
        optionsFile = open("../options.json","w")
        optionsFile.write(testoptions);
        
        pass


    def tearDown(self):
        #re-write the options file
        optionsFile = open("../options.json","w")
        optionsFile.write(self.old_options);
        
        pass

    def testInstallLinux64(self):
        self.assertEquals(OperatingSystem.LIN, self.j.getOperatingSystem(), "operating system did not detect as Linux")
        self.assertEquals(Architecture.x64, self.j.getArchitecture(), "architecture is not detected as x64")
        
        fsHelp = FileSystemHelper()
        os.system("python ../Jinn.py -install");
        
        #check for the existence of files
        #fsHelp.exists()
        pass
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()