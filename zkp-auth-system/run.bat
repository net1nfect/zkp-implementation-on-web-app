@echo off
echo ============================================================
echo ZKP Authentication System - Setup and Run
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Go to backend directory
cd backend

REM Run the application
echo ============================================================
echo Starting ZKP Authentication Server...
echo ============================================================
echo.
echo Server will be available at: http://localhost:5000
echo.
echo Press CTRL+C to stop the server
echo.
python app.py

pause

