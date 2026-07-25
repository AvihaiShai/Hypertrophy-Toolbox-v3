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

:: The build deliberately uses its own "venv", not the developer ".venv".
:: .venv has accumulated packages that requirements.txt never declares (pandas,
:: numpy), so building from it makes the artifact depend on incidental developer
:: state -- that is how the stale pandas/numpy hidden imports appeared to work.
:: A dedicated environment built only from the committed requirements files is
:: reproducible.

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
if exist "Hypertrophy-Toolbox.spec" del /q "Hypertrophy-Toolbox.spec"

:: Check if favicon exists, adjust command accordingly
set ICON_ARG=
if exist "static\images\favicon.ico" (
    set ICON_ARG=--icon=static/images/favicon.ico
)

:: Build the executable
echo.
echo [BUILD] Creating executable (this may take several minutes)...
echo.

venv\Scripts\pyinstaller.exe --name "Hypertrophy-Toolbox" ^
    --onedir ^
    --console ^
    %ICON_ARG% ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "data;data" ^
    --hidden-import=flask ^
    --hidden-import=jinja2 ^
    --hidden-import=werkzeug ^
    --hidden-import=openpyxl ^
    --hidden-import=xlsxwriter ^
    --collect-submodules=werkzeug ^
    --collect-submodules=jinja2 ^
    app_launcher.py

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
