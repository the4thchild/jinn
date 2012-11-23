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
        return super(JarResource, self).doInstall(True)