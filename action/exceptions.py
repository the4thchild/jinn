"""
Exception for when an Action couldn't be found
"""
class ActionNotFoundException(Exception):
    
    def __init__(self, value = None, os = None, arch = None):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
    
"""
Exception for when a piece of data was missing
"""
class ActionDataMissingException(Exception):
    
    def __init__(self, value = None, os = None, arch = None):
        self.value = value
    
    def __str__(self):
        return repr(self.value)