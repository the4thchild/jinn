import requests

class UrlLoader:
    
    def __init__(self, url):
        self.url = url
    
    """
    If you provide is_json, expect an object back or None
    If you do not or leave it out, expect a text string
    """
    def read(self, is_json = False):
        if self.url_contents == None:
            r = requests.get(self.url)
            if is_json:
                self.url_contents = r.json()
            else:
                self.url_contents = r.text()
        return self.url_contents
    
    def __del__(self):
        pass