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
    Alias for getDirectorySeparator
    """
    def sep(self):
        return self.getDirectorySeparator()
    
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
        return self.workWithFile(fname, content, "w")
        
    """
    Append content to a file
    """
    def appendToFile(self, fname, content):
        return self.workWithFile(fname, content, "a")
        
    """
    General file helper
    """
    def workWithFile(self, fname, content, mode):
        try:
            f = open(fname, mode)
            f.write(content)
            f.close()
            return True
        except:
            return False
    
    """
    Remove a specific content string from the specified file
    """
    def removeFromFile(self, fname, content):
        try:
            fin = open(fname)
            fout = open(fname + ".tmp", "w+")
            for line in fin:
                fout.write(line.replace(content, ""))
            fin.close()
            fout.close()
            self.rename(fname + ".tmp", fname)
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
        try:
            if os.path.isdir(path):
                g.feedback.log(LogLevels.DEBUG, "Path %s is a directory, deleting" % path)
                shutil.rmtree(path, onerror=onerror)
            elif os.path.islink(path):
                g.feedback.log(LogLevels.DEBUG, "Path %s is a symlink, unlinking" % path)
                os.unlink(path)
            elif os.path.exists(path):
                g.feedback.log(LogLevels.DEBUG, "Path %s is a file, deleting" % path)
                os.remove(path)
            return True
        except Exception as e:
            g.feedback.log(LogLevels.ERROR, "Unable to delete file or directory at %s: %s" % (path, e))
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
    
# http://stackoverflow.com/questions/2656322/python-shutil-rmtree-fails-on-windows-with-access-is-denied
def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise