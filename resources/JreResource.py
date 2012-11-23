from resource.ResourceBase import ResourceBase

class JreResource(ResourceBase):
    
    def getType(self):
        return "Jinn::Resource::Jre"
    
    def getPath(self):
        if not "Path" in self.properties:
            return "jre"
        else:
            return self.properties["Path"]
    
    def doInstall(self):
        file = self.doDownload(self.properties["Source"])
        if not "Path" in self.properties:
            self.properties["Path"] = "jre"
        # Delete the target dir if it exists already
        self.delete(self.properties["Path"])
        self.decompress(file, self.properties["Source"], self.properties["Path"])
        self.delete(file)
        return True