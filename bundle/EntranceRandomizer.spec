# -*- mode: python -*-
from PyInstaller.compat import is_win
block_cipher = None

# Todo: the runtime hooks should only be installed on windows
a = Analysis(['../EntranceRandomizer.py'],
             pathex=['bundle'],
             binaries=[],
             datas=[('../data/', 'data/'), ('../README.html', '.'), ('../LICENSE.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=['bundle/_rt_hook.py'],
             excludes=['lzma', 'bz2'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='EntranceRandomizer',
          debug=False,
          strip=False,
          upx=False,
          console=is_win )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='EntranceRandomizer')
app = BUNDLE(coll,
             name ='EntranceRandomizer.app',
             icon = None,
             bundle_identifier = None)
