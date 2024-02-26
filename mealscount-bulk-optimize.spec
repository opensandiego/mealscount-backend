# -*- mode: python ; coding: utf-8 -*-

import datetime

a = Analysis(
    ['mealscount-bulk-optimize.py'],
    pathex=['.\\venv\\Lib\\site-packages\\'],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
)
pyz = PYZ(a.pure, a.zipped_data)

datestamp = datetime.datetime.now().strftime("%Y%m%d")
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='mealscount-bulk-optimize-%s' % datestamp,
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
    icon=['mealscount_icon.ico'],
)
