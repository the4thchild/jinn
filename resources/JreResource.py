from resource.ResourceBase import ResourceBase

class JreResource(ResourceBase):
    
    def getType(self):
        return "Jinn::Resource::Jre"
    
    def getPath(self):
        if not "Path" in self.properties:
            return "jre"
        else:
            return self.getProperty("Path")
    
    def doInstall(self):
        return True
        # TODO: Change this to use the other downloaders/extracters
        f = self.doDownload(self.getProperty("Source"))
        if not "Path" in self.properties:
            self.properties["Path"] = "jre"
        # Delete the target dir if it exists already
        self.delete(self.getProperty("Path"))
        self.decompress(f, self.getProperty("Source"), self.getProperty("Path"))
        self.delete(f)
        return True