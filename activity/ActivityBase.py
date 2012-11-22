
"""
A base class for Resources and Actions
Defines methods that these types, through
ActionBase and ResourceBase, can implement
"""
class ActivityBase(object):
    
    # Properties of this activity
    properties = None
    
    # The OS context we are running in
    os = None
    
    # The architecture context we are running in
    arch = None
    
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
    
    """
    Initialises the activity with the os and architecture we are running under
    """
    def __init__(self, os, arch):
        self.os = os
        self.arch = arch