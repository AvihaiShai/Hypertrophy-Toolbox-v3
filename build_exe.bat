@echo off
setlocal enabledelayedexpansion
title Building Hypertrophy Toolbox Executable
color 0E

echo.
echo  ========================================
echo    BUILDING STANDALONE EXECUTABLE
echo  ========================================
echo.

:: Change to script directory
cd /d "%~dp0"
echo [INFO] Working directory: %cd%
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] %PYVER% found
echo.

:: The build deliberately uses "venv", not the developer ".venv".
:: .venv has accumulated packages that requirements.txt never declares (pandas,
:: numpy), so building from it makes the artifact depend on incidental developer
:: state -- that is how the stale pandas/numpy hidden imports appeared to work.
:: An environment built only from the committed requirements files is reproducible.
::
:: Note that "venv" is shared with START.bat, which creates it for end users and
:: installs only requirements.txt. So this environment is not isolated from the
:: user launcher, only from ".venv" -- what keeps the build reproducible is the
:: unconditional install of both requirements files below, which repairs a venv
:: that START.bat created with the runtime set alone.

:: Check if virtual environment exists, create if not
if not exist "venv" (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

:: Install runtime + build dependencies. Run unconditionally: the previous
:: "install only if flask is missing" check left stale environments untouched,
:: so a venv created before a requirements change silently kept building with
:: the old dependency set. pip is a no-op when everything is already satisfied.
echo [INFO] Installing runtime dependencies...
venv\Scripts\pip.exe install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install runtime dependencies!
    pause
    exit /b 1
)
echo [OK] Runtime dependencies installed
echo.

echo [INFO] Installing pinned build dependencies...
venv\Scripts\pip.exe install -r requirements-build.txt
if errorlevel 1 (
    echo [ERROR] Failed to install build dependencies!
    pause
    exit /b 1
)
venv\Scripts\python.exe -c "import PyInstaller; print('  PyInstaller ' + PyInstaller.__version__)"
echo [OK] Build dependencies installed
echo.

:: Clean previous builds
echo [INFO] Cleaning previous builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

:: Resolve the tracked-asset manifest before the long build starts. The spec
:: stages and verifies it again at build time -- that is the authoritative
:: check, since PyInstaller's --clean wipes build\ before executing the spec --
:: but failing here keeps a broken manifest from costing a full build first.
echo [INFO] Staging tracked package assets...
venv\Scripts\python.exe scripts\stage_package_assets.py
if errorlevel 1 (
    echo [ERROR] Package asset staging failed!
    pause
    exit /b 1
)
echo [OK] Package asset manifest verified
echo.

:: Build the executable
echo.
echo [BUILD] Creating executable (this may take several minutes)...
echo.

venv\Scripts\pyinstaller.exe --clean --noconfirm Hypertrophy-Toolbox.spec

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

:: Copy the run script to dist folder
copy "RUN_APP.bat" "dist\Hypertrophy-Toolbox\" >nul

echo.
echo  ========================================
echo    BUILD COMPLETE!
echo  ========================================
echo.
echo  Your executable is in: dist\Hypertrophy-Toolbox\
echo.
echo  To distribute:
echo    1. Zip the entire "dist\Hypertrophy-Toolbox" folder
echo    2. Share the zip file with users
echo    3. Users extract and double-click "Hypertrophy-Toolbox.exe"
echo.
pause
