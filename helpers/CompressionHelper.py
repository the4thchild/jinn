import g
from feedback.LogLevels import LogLevels
from zipfile import ZipFile
import tarfile
from FileSystemHelper import FileSystemHelper

"""
Compression helper for helping to do compression stuff quickly 
"""
class CompressionHelper(FileSystemHelper):
    
    """
    Returns the compression type from the filename
    """
    def getCompressionType(self, filename):
        if filename.endswith(".tar.gz"):
            return CompressionType.TARGZ
        elif filename.endswith(".pack.jar"):
            return CompressionType.PACK200
        elif filename.endswith(".zip"):
            return CompressionType.ZIP
        else:
            return None

    """
    Decompress a file
    Use this when your file name specifies the compression type
    """
    def decompressFile(self, filename, path = "."):
        return self.decompress(filename, filename, path)


    """
    Decompresses the file at filename
    nameforcompression is the string to use to figure out what type of compression to use
    Use this when your filename doesnt specify the encoding type but you have another string that does
    """
    def decompress(self, filename, nameforcompression, path = "."):
        t = self.getCompressionType(nameforcompression)
        
        if t is None:
            # Found no compression, so don't need to do anything
            g.feedback.log(LogLevels.DEBUG, "File %s does not have any compression on it" % filename)
            return True
        
        # Make the directory to extract to if it does not yet exist
        if path is not ".":
            if not self.makeDirectory(path):
                return False
            
        if t is CompressionType.ZIP:
            # TODO: Test this works
            ZipFile(filename).extractall(path)
            return True
        elif t is CompressionType.TARGZ:
            tar = tarfile.open(filename)
            tar.extractall(path)
            tar.close()
            return True
        elif t is CompressionType.PACK200:
            # TODO: Implement pack 200
            g.feedback.log(LogLevels.ERROR, "Pack 200 not yet implemented")
            return False
        else:
            g.feedback.log(LogLevels.ERROR, "Compression type %s is not currently supported" % str(type))
            return False

class CompressionType(object):
    TARGZ = 1
    PACK200 = 2
    ZIP = 3