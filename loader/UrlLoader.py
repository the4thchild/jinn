import requests
from LoaderBase import LoaderBase

class UrlLoader(LoaderBase):
    
    def read(self, is_json = False):
        if self.cache == None:
            r = requests.get(self.location)
            if is_json:
                self.cache = r.json
            else:
                self.cache = r.text
        return self.cache