# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['scormTester.py'],
             pathex=['C:\\Users\\timop\\PycharmProjects\\scorm-tester'],
             binaries=[],
             datas=[('writeExcel.py', '.'), ('xmlHelper.py', '.'), ('scormZipper.py', '.'), ('mediainfo.py', '.'), ('exiftool.exe', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='scormTester',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='schwarz.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='scormTester')
