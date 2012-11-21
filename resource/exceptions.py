"""
Exception for when a resource couldn't be found
"""
class ResourceNotFoundException(Exception):
    
    def __init__(self, value = None, os = None, arch = None):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
    
"""
Exception for when a piece of data was missing
"""
class ResourceDataMissingException(Exception):
    
    def __init__(self, value = None, os = None, arch = None):
        self.value = value
    
    def __str__(self):
        return repr(self.value)