@echo off
cd /d "%~dp0"
cd ..\ 
python "%~dp0run_debug_gym.py"
if errorlevel 1 (
    echo.
    echo Press any key to close...
    pause >nul
)