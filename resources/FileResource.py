from resource.ResourceBase import ResourceBase

class FileResource(ResourceBase):
    
    # The file name for the downloaded resource
    filename = None
    
    def getType(self):
        return "Jinn::Resource::File"
    
    def doInstall(self, usePath = True):
        if "Path" in self.properties and usePath:
            path = self.properties["Path"]
        else:
            path = None
        if path is not None and not self.makeDirectory(path):
            return False
        self.filename = self.doDownload(self.properties["Source"], path)
        return True