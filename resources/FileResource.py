import g
from resource.ResourceBase import ResourceBase
from feedback.LogLevels import LogLevels

class FileResource(ResourceBase):
    
    def getType(self):
        return "Jinn::Resource::File"
    
    def doInstall(self):
        if "Path" in self.properties:
            path = self.getPathFromFilePath(self.properties["Path"])
        else:
            path = None
        if path is not None and not self.makeDirectory(path):
            return False
        self.doDownload(self.properties["Source"], path)
        return True