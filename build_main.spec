# -*- mode: python -*-

import os

block_cipher = None

is_one_file = False
a = Analysis(['main.py'],
             pathex=[os.getcwd(), r'C:\Program Files (x86)\DrExplain'],
             binaries=[],
             datas=[('UI\\*.ui', 'UI')],
             hiddenimports=['tkinter', 'tkinter.filedialog'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

if is_one_file:
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              name='main',
              debug=True,
              strip=False,
              icon='ico.ico',
              upx=True,
              console=True )
else:
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='main',
              debug=False,
              strip=False,
              upx=True,
              console=False,
              icon='ico.ico')

    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   name='main')
