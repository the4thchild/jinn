import g
from resource.ResourceBase import ResourceBase
from feedback.LogLevels import LogLevels

class FileResource(ResourceBase):
    
    def getType(self):
        return "Jinn::Resource::File"
    
    def doInstall(self):
        path = self.getPathFromFilePath(self.properties["Path"])
        if len(path) > 0 and not self.makeDirectory(path):
            g.feedback.log(LogLevels.ERROR, "Unable to create path %s" % path)
            return False
        self.doDownload(self.properties["Source"], self.properties["Path"])
        return True