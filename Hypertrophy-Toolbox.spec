# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

REPO_ROOT = Path(SPECPATH).resolve()  # noqa: F821 - injected by PyInstaller
sys.path.insert(0, str(REPO_ROOT))

from scripts.stage_package_assets import staged_datas  # noqa: E402

# pandas/numpy were dropped when the exporters moved to XlsxWriter directly
# (see routes/exports.py and utils/export_utils.py) and are not declared in
# requirements.txt; listing them here only produced build-time resolution errors.
# xlsxwriter is imported lazily inside functions, so it must stay declared here.
hiddenimports = ['flask', 'jinja2', 'werkzeug', 'openpyxl', 'xlsxwriter']
hiddenimports += collect_submodules('werkzeug')
hiddenimports += collect_submodules('jinja2')

approved_data_files = [
    ('data/catalog.seed.db', 'data'),
    ('data/free_exercise_db_mapping.csv', 'data'),
]


# static/ and templates/ are collected from a staging tree rebuilt from
# `git ls-files`, not from a filesystem walk. Ignored and untracked working-copy
# content (the GPT body-map scratch root and its nested .git among it) is absent
# from the manifest, so it cannot be packaged and needs no exclusion list.
# staged_datas() fails closed if the staged tree diverges from tracked sources.
asset_files = staged_datas(REPO_ROOT)

# Minimal excludes - only things definitely not needed (prioritize performance over size)
excludes = [
    'tkinter', 'matplotlib', 'scipy', 'PIL', 'IPython',
    'notebook', 'jupyter', 'pytest', 'hypothesis'
]

a = Analysis(
    ['app_launcher.py'],
    pathex=[],
    binaries=[],
    datas=asset_files + approved_data_files,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=True,  # Keep .pyc files separate - faster startup (no archive extraction)
    optimize=2,  # Bytecode optimization (removes docstrings/asserts)
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Hypertrophy-Toolbox',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX - improves startup time (no decompression needed)
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['static\\images\\favicon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,  # Disable UPX for faster startup
    upx_exclude=[],
    name='Hypertrophy-Toolbox',
)
