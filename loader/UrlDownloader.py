import urllib

"""
Downloads a file from a URL onto a target file name
"""
class UrlDownloader(object):

    def __init__(self, url):
        self.file = None
        
        self.url = url
        
    """
    Do the download and save it to the file
    Returns the filename
    """
    def download(self, file):
        self.file = file
        urllib.urlretrieve(self.url, self.file)
        return self.file