# -*- mode: python -*-
   
def Bitness():
    if(sys.maxsize > 2**32) :
        return "x64"
    else :
        return "x32"

a = Analysis(['Jinn.py', 'options.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'Jinn-linux-' + Bitness()),
          debug=False,
          strip=True,
          upx=True,
          console=True)
