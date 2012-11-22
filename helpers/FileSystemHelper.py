import os
import shutil
import sys

"""
A helper class for doing common things on the filesystem
"""
class FileSystemHelper(object):
    
    """
    Check whether or not the directory exists
    If something with that name exists but is not directory, returns false
    """
    def directoryExists(self, directory):
        return os.path.isdir(directory)
    
    """
    Return the current working directory
    """
    def getCurrentDirectory(self):
        return os.getcwd()
    
    """
    Make directory
    """
    def makeDirectory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            return True
        except:
            return False;
            
    """
    Return the home directory of the user
    """
    def getHomeDirectory(self):
        return os.path.expanduser("~")
    
    """
    Returns the os separator
    """
    def getDirectorySeparator(self):
        return os.sep
    
    """
    Change to the target directory
    """
    def changeDirectory(self, directory):
        try:
            os.chdir(directory)
            return True
        except:
            return False
        
    """
    Copy a file from one filename to another filename
    """
    def copyFile(self, frm, to):
        try:
            shutil.copy2(frm, to)
            return True
        except:
            return False
        
    """
    Return the file that is running this script
    """
    def getCurrentFile(self):
        return sys.argv[0]
    
    """
    Helper to save some data to a file
    """
    def saveToFile(self, file, content):
        try:
            f = open(file, 'w')
            f.write(content)
            f.close()
            return True
        except:
            return False
        
    """
    Helper to get the file name given a path to a file
    """
    def getFileNameFromPath(self, path):
        path,file=os.path.split(path)
        return file
    
    """
    Helper to get path from a file with path location
    """
    def getPathFromFilePath(self, path):
        path,file=os.path.split(path)
        return path