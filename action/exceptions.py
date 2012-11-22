"""
Exception for when a piece of data was missing
"""
class ActionDataMissingException(Exception):
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)