from ArchiveResource import ArchiveResource

class JarResource(ArchiveResource):
    
    def getType(self):
        return "Jinn::Resource::Jar"

    def getNewFileName(self):
        return self.getProperty("Path") + self.getDirectorySeparator() + self.getProperty("Name")

    def doInstall(self):
        # Download and extract
        super(JarResource, self).doInstall(".", "jar")
        
        # Rename the file from the current one to what it should be
        current = "." + self.getDirectorySeparator() + "jar"
        new = self.getNewFileName()
        
        # Check the directory is installed
        self.makeDirectory(self.getProperty("Path"))
        
        return self.rename(current, new)
    
    def doUninstall(self):
        return self.delete(self.getNewFileName())