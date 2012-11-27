from resource.ResourceBase import ResourceBase

class FileResource(ResourceBase):
    
    # The file name for the downloaded resource
    filename = None
    
    def getType(self):
        return "Jinn::Resource::File"
    
    def doInstall(self, path = None, name = None):
        if path is None and "Path" in self.properties:
            path = self.getProperty("Path")
            
        if path is not None and not self.makeDirectory(path):
            return False
        
        if name is None and "Name" in self.properties:
            name = self.getProperty("Name")
        
        self.filename = self.doDownload(self.getProperty("Source"), path, name)
        return True