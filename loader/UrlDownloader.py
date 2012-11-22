import urllib

"""
Downloads a file from a URL onto a target file name
"""
class UrlDownloader(object):
    
    # The URL of the resource
    url = None
    
    # The name of the file it is saved to
    file = None
    
    """
    Init with the URL we want to download
    """
    def __init__(self, url):
        self.url = url
        
    """
    Do the download and save it to the file
    Returns the filename
    """
    def download(self, file):
        self.file = file
        urllib.urlretrieve(self.url, self.file)
        return self.file