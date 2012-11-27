from ArchiveResource import ArchiveResource

class JarResource(ArchiveResource):
    
    # The file name of the downloaded resource
    filename = None
    
    def getType(self):
        return "Jinn::Resource::Jar"

    def doInstall(self):
        # Download and extract
        super(JarResource, self).doInstall(".", "jar")
        
        # Rename the file from the current one to what it should be
        current = "." + self.getDirectorySeparator() + "jar"
        new = self.getProperty("Path") + self.getDirectorySeparator() + self.getProperty("Name")
        
        # Check the directory is installed
        self.makeDirectory(self.getProperty("Path"))
        
        return self.rename(current, new)