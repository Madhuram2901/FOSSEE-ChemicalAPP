@echo off
REM Quick start script for Chemical Equipment Visualizer Desktop App

echo ========================================
echo Chemical Equipment Visualizer Desktop
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install/update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo.

REM Check if backend is running
echo Checking backend connection...
python -c "import requests; requests.get('http://localhost:8000/api/', timeout=2)" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Backend server is not running!
    echo Please start the backend in another terminal:
    echo   cd ..\backend
    echo   python manage.py runserver
    echo.
    echo Press any key to continue anyway, or Ctrl+C to exit...
    pause >nul
)

REM Start the application
echo Starting desktop application...
echo.
C:\Users\Madhuram\AppData\Local\Programs\Python\Python310\python.exe main.py

REM Deactivate on exit
deactivate
