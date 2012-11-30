'''
Created on 30 Nov 2012

@author: dev
'''
import unittest
import g
import platform
import os

from env.enums import OperatingSystem, Architecture
from feedback.LogLevels import LogLevels
from feedback.ConsoleFeedback import ConsoleFeedback
from helpers import FileSystemHelper


class Test(unittest.TestCase):


    def setUp(self):
        
        self.fsHelp = FileSystemHelper()
        #save a copy of the original options file
        self.old_options = "manifest=\"manifests/import_manifest.json\"\n# TODO: Get rid of this\nmanifest_is_url = False\ninterface = \"cmd\"\nversion = \"DEV\""
        
        pass


    def tearDown(self):
        #re-write the options file
        optionsFile = open("../options.py","w")
        optionsFile.write(self.old_options);
        optionsFile.close()
        pass
    
    #the names of these tests are to keep the order consistent
    # test to install an archive resource
    def testA_InstallSingleArchiveResource(self):
        

        self.setManifest("manifests/archive_manifest.json")
        
        self.setUpOS()
        
        os.system("python ../Jinn.py -install");
        
        #check for the existence of files
        if(self.os == OperatingSystem.LIN):
            if(self.arch == Architecture.x64):
                self.checkExistsLinux64()
                pass
            if(self.arch == Architecture.x32):
                self.checkExistsLinux32()
        
        
        pass
    
    # test to uninstall an archive resource
    def testB_UninstallSingleArchiveResource(self):
        

        self.setManifest("manifests/archive_manifest.json")
        
        self.setUpOS()
        
        os.system("python ../Jinn.py -uninstall");
        
        #check for the existence of files
        if(self.os == OperatingSystem.LIN):
            if(self.arch == Architecture.x64):
                self.checkDeletedLinux64()
                pass
            if(self.arch == Architecture.x32):
                self.checkDeletedLinux32()
        
        
        pass
    
    #def testUpdateSingleResource(self):
        
    #    pass
    
    def checkExistsLinux64(self):
        self.assertTrue(self.fsHelp.exists("../TestData/examples"))
        pass
    
    def checkExistsLinux32(self):
        self.assertTrue(self.fsHelp.exists("../TestData/examples"))
        pass
    
    def checkDeletedLinux64(self):
        self.assertFalse(self.fsHelp.exists("../TestData/examples"))
        self.assertFalse(self.fsHelp.exists("../TestData"))
        self.assertFalse(self.fsHelp.exists("../.jinn"))
        pass
    
    def checkDeletedLinux32(self):
        self.assertFalse(self.fsHelp.exists("../TestData/examples"))
        self.assertFalse(self.fsHelp.exists("../TestData"))
        self.assertFalse(self.fsHelp.exists("../.jinn"))
        pass
    
    def setManifest(self, path):
        #out new options file with the test manifest
        testoptions = "manifest=\""+path+"\"\n# TODO: Get rid of this\nmanifest_is_url = False\ninterface = \"cmd\"\nversion = \"DEV\""
        
        optionsFile = open("../options.py","w")
        optionsFile.write(testoptions);
        optionsFile.close()
        pass

    def setUpOS(self):
        import Jinn
        self.j = Jinn.Jinn()
        
        self.os = self.j.getOperatingSystem()
        self.arch = self.j.getArchitecture()
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()