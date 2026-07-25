# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

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


def collect_asset_tree(source, destination, excluded_subtree=None):
    source_root = Path(source)
    excluded_root = (
        (source_root / excluded_subtree).resolve()
        if excluded_subtree
        else None
    )
    assets = []
    for asset in source_root.rglob('*'):
        if not asset.is_file():
            continue
        resolved = asset.resolve()
        if excluded_root and (
            resolved == excluded_root or excluded_root in resolved.parents
        ):
            continue
        relative_parent = asset.relative_to(source_root).parent
        target = (Path(destination) / relative_parent).as_posix()
        assets.append((asset.as_posix(), target))
    return assets


template_assets = collect_asset_tree('templates', 'templates')
static_assets = collect_asset_tree(
    'static',
    'static',
    excluded_subtree='bodymaps/GPT/',
)

# Minimal excludes - only things definitely not needed (prioritize performance over size)
excludes = [
    'tkinter', 'matplotlib', 'scipy', 'PIL', 'IPython', 
    'notebook', 'jupyter', 'pytest'
]

a = Analysis(
    ['app_launcher.py'],
    pathex=[],
    binaries=[],
    datas=template_assets + static_assets + approved_data_files,
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
