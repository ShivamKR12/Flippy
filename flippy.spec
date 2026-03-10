# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['flippy.py'],
    pathex=[],
    binaries=[],
    datas=[('flippyboard.png', 'flippyboard.png'), ('flippybackground.png', 'flippybackground.png'), ('flippylogo.png', 'flippylogo.png')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='flippy',
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
    icon='flippyicon.ico',
)
