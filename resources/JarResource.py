from ArchiveResource import ArchiveResource

class JarResource(ArchiveResource):
    
    def getType(self):
        return "Jinn::Resource::Jar"
    
    """
    Override the doDownload to make sure
    the path is not passed through so a temporary
    file is generated
    """
    def doDownload(self, source, path):
        return super(JarResource, self).doDownload(source, None)
    
    def doInstall(self):
        # Download and extract
        super(JarResource, self).doInstall(True)
        
        # Rename the file from the current one to what it should be
        current = self.getPathFromFilePath(self.properties["Path"]) + self.getDirectorySeparator() + self.filename.replace(".pack.gz", "")
        new = self.properties["Path"]
        return self.rename(current, new)