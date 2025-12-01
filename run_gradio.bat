@echo off
pause

python gradio_app.py
cd src
echo Starting ChatPPT Gradio application...
echo.

pip install -q -r requirements.txt
echo Installing/Updating required packages...
echo.

)
    exit /b 1
    pause
    echo ERROR: Python is not installed or not in PATH
if errorlevel 1 (
python --version
echo Checking Python environment...

cd /d %~dp0

echo.
echo ========================================
echo  ChatPPT Gradio Application Launcher
echo ========================================

