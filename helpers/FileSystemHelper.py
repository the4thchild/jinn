import os
import shutil
import sys
import g
from feedback.LogLevels import LogLevels

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
    Returns whether or not the path exists
    Could be a directory or a file
    """
    def exists(self, path):
        return os.path.exists(path)
    
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
            if not os.path.isdir(directory):
                os.makedirs(directory)
            return True
        except:
            g.feedback.log(LogLevels.ERROR, "Unable to create path %s" % directory)
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
    def saveToFile(self, fname, content):
        try:
            f = open(fname, 'w')
            f.write(content)
            f.close()
            return True
        except:
            return False
        
    """
    Helper to get the file name given a path to a file
    """
    def getFileNameFromPath(self, path):
        p,f = os.path.split(path)
        return f
    
    """
    Helper to get path from a file with path location
    """
    def getPathFromFilePath(self, path):
        p,f = os.path.split(path)
        return p
    
    """
    Deletes a file or directory at the specified location
    """
    def delete(self, path):
        # TODO: Does this work with Symlinks? To folders / files?
        try:
            if os.path.isdir(path):
                # Delete if a directory
                shutil.rmtree(path)
            elif os.path.exists(path):
                # Delete if a file
                os.remove(path)
            return True
        except:
            g.feedback.log(LogLevels.ERROR, "Unable to delete file or directory at %s" % path)
            return False
        
    """
    Rename a file or directory
    Deletes the target first if it exists
    """
    def rename(self, frm, to):
        try:
            self.delete(to)
            os.rename(frm, to)
            return True
        except:
            return False