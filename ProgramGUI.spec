# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['ProgramGUI.py'],
    pathex=[],
    binaries=[('s3pi/s3pi.Interfaces.dll', '.'),
              ('s3pi/s3pi.WrapperDealer.dll', '.'),
              ('s3pi/s3pi.Package.dll', '.'),
              ('s3pi/s3pi.DefaultResource.dll', '.'),
              ('C:\\Users\\yenching\\AppData\\Roaming\\Python\\Python310\\site-packages\\customtkinter', 'customtkinter')
             ],
    datas=[('assets/icon.ico', 'assets'),
           ('assets/energy.png', 'assets'),
           ('assets/open-folder.png', 'assets')],
    hiddenimports=['clr'],
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
    name='Sims3PatternRecategorizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
