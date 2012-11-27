from FileResource import FileResource
from feedback.LogLevels import LogLevels
import g

class ArchiveResource(FileResource):
    
    def getType(self):
        return "Jinn::Resource::Archive"
    
    def doInstall(self, pathIsFile = False):
        # Do the download with the file resource
        super(ArchiveResource, self).doInstall(pathIsFile)
        
        # Get the downloaded filename
        fname = self.filename
        
        # Check if there is compression. If so, decompress it
        if self.getCompressionType(self.getProperty("Source")) is not None:
            g.feedback.log(LogLevels.DEBUG, "File is compressed so decompressing")
            
            # Get the right path value
            if "Path" in self.properties:
                path = self.getProperty("Path")
            else:
                path = "."
                
            if not self.decompress(fname, self.getProperty("Source"), path, pathIsFile):
                return False
            # Once we have decompressed it, delete the downloaded archive
            if not self.delete(fname):
                return False
        return True