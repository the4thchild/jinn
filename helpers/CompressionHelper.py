import g
import os
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
        elif filename.endswith(".pack.gz"):
            return CompressionType.PACK200
        elif filename.endswith(".zip"):
            return CompressionType.ZIP
        else:
            return None

    """
    Helper to decompress a file which we know has the right extension
    """
    def decompressFile(self, file, path = "."):
        return self.decompress(file, file, path, None)

    """
    Decompresses the file at filename
    nameforcompression is the string to use to figure out what type of compression to use
    Use this when your filename doesnt specify the encoding type but you have another string that does
    Specify the file name if you want to extract a compatible unpack (e.g. unpack200) to a specific name
    """
    def decompress(self, filename, nameforcompression, path = ".", name = None):
        t = self.getCompressionType(nameforcompression)
        
        if t is None:
            # Found no compression, so don't need to do anything
            g.feedback.log(LogLevels.DEBUG, "File %s is not compressed" % filename)
            return True
        
        # Make the directory to extract to if it does not yet exist
        if path is not "." and not self.makeDirectory(path):
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
            # Check there is a valid manifest file
            if self.manifest is None:
                g.feedback.log(LogLevels.ERROR, "Pack200 not available, no manifest in this helper instance")
                return False
        
            # Attempt to load a JRE resource
            res = self.manifest.getResourceForType("Jinn::Resource::Jre")
            if res is None:
                g.feedback.log(LogLevels.ERROR, "Pack200 not available, no JRE found in the project")
                return False
            
            # Check the JRE is installed, does the check in the method
            res.doInstall()
            
            # Check the unpack exists
            unpacker = res.type.getPath() + self.getDirectorySeparator() + "bin" + self.getDirectorySeparator() + "unpack200"
            if not self.exists(unpacker):
                g.feedback.log(LogLevels.ERROR, "Pack200 not available, JRE found but unable to find unpack200 in the bin path: %s" % unpacker)
                return False
            
            if name is not None:
                target = path + self.getDirectorySeparator() + name
            else:
                target = path + self.getDirectorySeparator() + filename.replace(".pack.gz", "")
            
            cmd = unpacker + " " + filename + " " + target
            result = os.system(cmd)
            if result > 0:
                g.feedback.log(LogLevels.ERROR, "Return code from unpacker is %s, unpack command: %s" % (result, cmd))
                return False
            else:
                return True
        else:
            g.feedback.log(LogLevels.ERROR, "Compression type %s is not currently supported" % str(type))
            return False

class CompressionType(object):
    TARGZ = 1
    PACK200 = 2
    ZIP = 3