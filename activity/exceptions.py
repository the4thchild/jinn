"""
Exception for when an Action couldn't be found
"""
class ActivityNotFoundException(Exception):
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
    