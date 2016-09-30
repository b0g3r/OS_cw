# -*- mode: python -*-

block_cipher = None


a = Analysis(['--paths C:\\Python35-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'main.spec'],
             pathex=['C:\\Users\\kotvb_000\\PycharmProjects\\OS_kr'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='bin',
          debug=False,
          strip=False,
          upx=True,
          console=False )
