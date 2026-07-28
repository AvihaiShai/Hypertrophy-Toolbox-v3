@echo off
setlocal enabledelayedexpansion
title Hypertrophy Toolbox
color 0A

echo.
echo  ========================================
echo     HYPERTROPHY TOOLBOX - LAUNCHER
echo  ========================================
echo.

:: Change to the script's directory
cd /d "%~dp0"
echo [INFO] Working directory: %cd%
echo.

:: Read the canonical pin and select its registered Python minor explicitly.
:: This keeps the launcher stable even if another project changes the global
:: "python" PATH order.
if not exist ".python-version" (
    echo [ERROR] Missing .python-version runtime contract!
    pause
    exit /b 1
)
set /p PYTHON_VERSION=<.python-version
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do set "PYTHON_TAG=%%a.%%b"
set "PYTHON_CMD=py -%PYTHON_TAG%"

:: Check if the required Python minor is registered.
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Registered Python %PYTHON_TAG% is not installed!
    echo.
    echo Please install Python %PYTHON_VERSION% or newer from:
    echo https://www.python.org/downloads/release/python-3146/
    echo Make sure the Python launcher or install manager is enabled.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYVER=%%i
echo [OK] %PYVER% found
echo.

:: Enforce the repository's canonical minimum before creating or reusing a venv.
%PYTHON_CMD% -m utils.python_version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Hypertrophy Toolbox requires Python %PYTHON_VERSION% or newer.
    echo Update the registered Python %PYTHON_TAG% runtime and try again.
    echo.
    pause
    exit /b 1
)

:: A venv keeps the interpreter it was created with. Refuse an older retained
:: environment instead of silently running it after the registered runtime changes.
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe -m utils.python_version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] The existing "venv" was created with Python older than 3.14.6.
        echo Delete the "venv" folder and run START.bat again.
        echo.
        pause
        exit /b 1
    )
)

:: Check if virtual environment exists
if not exist "venv" (
    echo [SETUP] Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

:: Check if dependencies are installed (check for Flask)
echo [INFO] Checking dependencies...
venv\Scripts\python.exe -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [SETUP] Installing dependencies - this may take 1-2 minutes...
    echo.
    venv\Scripts\pip.exe install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencies installed
    echo.
) else (
    echo [OK] Dependencies already installed
    echo.
)

:: Set port
set PORT=5000

echo  ========================================
echo    Starting Hypertrophy Toolbox...
echo  ========================================
echo.
echo    URL: http://127.0.0.1:%PORT%
echo.
echo    The browser will open automatically.
echo    If not, manually open the URL above.
echo.
echo    Press Ctrl+C to stop the server.
echo  ========================================
echo.

:: Open browser after delay (use start command directly)
start "" cmd /c "ping -n 4 127.0.0.1 >nul && start http://127.0.0.1:%PORT%"

:: Run the Flask app using the venv python explicitly
echo [INFO] Starting Flask server...
echo.
venv\Scripts\python.exe app.py

:: If we get here, server stopped
echo.
echo [INFO] Server stopped.
pause
