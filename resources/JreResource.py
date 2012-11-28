from ArchiveResource import ArchiveResource

class JreResource(ArchiveResource):
    
    def getType(self):
        return "Jinn::Resource::Jre"
    
    def getPath(self):
        if not "Path" in self.properties:
            return "jre"
        else:
            return self.getProperty("Path")
    
    def doInstall(self):
        return super(JreResource, self).doInstall()
    
    def doUninstall(self):
        return super(JreResource, self).doUninstall()