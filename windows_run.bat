:: Made with ChatGPT!!!

@echo off
setlocal

:: --- SETTINGS ---
set "REQUIRED_PYTHON=3.10"
set "REQUIREMENTS_FILE=requirements.txt"
set "MAIN_SCRIPT=main.py"

:: --- Check Python ---
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH. Please install Python %REQUIRED_PYTHON% or newer.
    pause
    exit /b 1
)

:: --- Check Python version ---
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
for /f "tokens=1,2 delims=." %%a in ("%PY_VER%") do (
    set "PY_MAJOR=%%a"
    set "PY_MINOR=%%b"
)
if %PY_MAJOR% LSS 3 (
    echo [ERROR] Python %REQUIRED_PYTHON% or newer is required. Found Python %PY_VER%.
    pause
    exit /b 1
)
if %PY_MAJOR%==3 if %PY_MINOR% LSS 10 (
    echo [ERROR] Python %REQUIRED_PYTHON% or newer is required. Found Python %PY_VER%.
    pause
    exit /b 1
)

:: --- Check pip ---
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed. Please install pip for your Python.
    pause
    exit /b 1
)

:: --- Install dependencies ---
echo [INFO] Installing dependencies from %REQUIREMENTS_FILE%...
python -m pip install -r %REQUIREMENTS_FILE%
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies. Please check %REQUIREMENTS_FILE%.
    pause
    exit /b 1
)

:: --- Run the project ---
echo [INFO] Launching the project...
start "" pythonw %MAIN_SCRIPT%
exit /b 0

endlocal
pause
