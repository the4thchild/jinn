import json

class FileLoader:
    
    # The file handler object
    file = None
    
    # Cache for contents of the file
    file_contents = None
    
    # Name of the file
    file_name = None
    
    def __init__(self, filename):
        self.file_name = filename
        self.file = open(filename)
    
    def read(self, is_json):
        if self.file_contents == None:
            file_contents = ""
            for line in self.file:
                file_contents += line
            if is_json:
                try:
                    file_contents = json.loads(file_contents)
                except ValueError:
                    file_contents = None
            self.file_contents = file_contents
        return self.file_contents
    
    def __del__(self):
        self.file.close()