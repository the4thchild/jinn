from FileResource import FileResource
from feedback.LogLevels import LogLevels
import g

class ArchiveResource(FileResource):
    
    def getType(self):
        return "Jinn::Resource::Archive"
    
    def doInstall(self, path = None, name = None):
        # Set up a tmpname to download to, if name is provided
        if name is not None:
            tmpname = name + "tmp"
        else:
            tmpname = name
        
        # Do the download with the file resource
        super(ArchiveResource, self).doInstall(path, tmpname)
        
        # Check if there is compression. If so, decompress it
        source = self.getProperty("Source")
        if self.getCompressionType(source) is not None:
            g.feedback.log(LogLevels.DEBUG, "File from %s is compressed so decompressing" % source)
            
            # Get the right path value
            if path is None and "Path" in self.properties:
                path = self.getProperty("Path")
            else:
                path = "."
                
            if name is None and "Name" in self.properties:
                name = self.getProperty("Name")
                
            if not self.decompress(self.filename, self.getProperty("Source"), path, name):
                return False
            # Once we have decompressed it, delete the downloaded archive
            if not self.delete(self.filename):
                return False
        return True
    
    def doUninstall(self):
        # If we have a path, we can specifically delete it, otherwise will have to be cleaned up later
        if "Path" in self.properties:
            return self.delete(self.getProperty("Path"))
        else:
            g.feedback.log(LogLevels.DEBUG, "Archive does not have a path specified so can't auto-delete, will be cleaned up later")