from manifest.exceptions import VersionDataMissingException

class JinnVersion(object):

    def __init__(self, data):
        self.name = None
        self.version = None
        self.source = None
        self.updater = None
        
        self.data = data;
        
        self.load()
    
    def load(self):
        try:
            self.name = self.data["AppName"]
            self.version = self.data["Version"]
        except KeyError as e:
            raise VersionDataMissingException("Unable to find the required key %s" % e)