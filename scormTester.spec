# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['scormTester.py'],
    pathex=[],
    binaries=[],
    datas=[('writeExcel.py', '.'), ('xmlHelper.py', '.'), ('scormZipper.py', '.'), ('mediainfo.py', '.'), ('gui.py', '.'), ('exiftool.exe', '.'), ('run_20.js', '.'), ('run_21.js', '.'), ('disable_time_score.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='scormTester',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='schwarz.ico',
)
