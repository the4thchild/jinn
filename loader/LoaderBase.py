
"""
Base class for loaders
"""
class LoaderBase(object):

    def __init__(self, location):
        self.cache = None
        
        self.location = location
    
    """
    If you provide is_json, expect an object back or None
    If you do not or leave it out, expect a text string
    """
    def read(self, is_json = False):
        return None