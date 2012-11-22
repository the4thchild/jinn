import json
from LoaderBase import LoaderBase

class FileLoader(LoaderBase):
    
    # The file handler object
    file = None
    
    def __init__(self, location):
        super(FileLoader, self).__init__(location)
        self.file = open(self.location)
    
    def read(self, is_json = False):
        if self.cache == None:
            file_contents = ""
            for line in self.file:
                file_contents += line
            if is_json:
                try:
                    file_contents = json.loads(file_contents)
                except ValueError:
                    file_contents = None
            self.cache = file_contents
        return self.cache
    
    def __del__(self):
        self.file.close()