from resource.ResourceBase import ResourceBase

class FileResource(ResourceBase):
    
    def __init__(self, os, arch):
        self.filename = None
        
        super(FileResource, self).__init__(os, arch)
    
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
    
    def doUninstall(self):
        # This will only ever be called on file downloads so we can delete from the known source/path/file
        if "Path" in self.properties:
            path = self.properties["Path"]
        else:
            path = "."
            
        if "Name" in self.properties:
            name = self.properties["Name"]
        else:
            name = self.getFilenameFromUrl(self.getProperty("Source"))
            
        return self.delete(path + self.sep() + name)
    
    def isUpdatable(self, old_self):
        return self.getProperty("Source") != old_self.getProperty("Source")