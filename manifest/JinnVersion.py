from manifest.exceptions import VersionDataMissingException

class JinnVersion(object):
    
    # Data for the version from the configuration
    data = None
    
    # The version of the jinn
    version = None
    
    # The source of the jinn (URL)
    source = None
    
    # The updater to update the jinn
    updater = None
    
    def load(self):
        try:
            self.version = self.data["Version"]
            self.source = self.data["Source"]
            self.updater = self.data["Updater"]
        except KeyError as e:
            raise VersionDataMissingException("Unable to find the required key %s" % e)
    
    def __init__(self, data):
        self.data = data;
        self.load()