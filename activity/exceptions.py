"""
Exception for when an Action couldn't be found
"""
class ActivityNotFoundException(Exception):
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
    
"""
Exception for when a required property can't be found
"""
class RequiredPropertyNotFound(Exception):
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)