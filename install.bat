@echo off
echo Installing Rebol 3 Script Analysis Tool...
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo Installing Flask...
pip install flask

echo.
echo Installation complete!
echo.
echo To run the application:
echo   python app.py
echo.
echo Then open your browser to: http://localhost:5000
echo.
pause