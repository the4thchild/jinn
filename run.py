import sys
import options

from manifest.Manifest import Manifest

"""
Main function that is run when the code is started from this file
"""
def main():
    manifest = Manifest(options.manifest, options.manifest_is_url)
    print manifest

if __name__ == '__main__':
    status = main()
    sys.exit(status)