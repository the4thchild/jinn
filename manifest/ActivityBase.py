
"""
A base class for Resources and Actions
Defines methods that these types, through
ActionBase and ResourceBase, can implement
"""
class ActivityBase:
    
    properties = None
    
    """
    Provides the ability to load properties from configuration file
    """
    def loadProperties(self, properties):
        self.properties = properties;
        print properties
    
    """
    Return the type string this Activity corresponds to
    """
    def getType(self):
        return None