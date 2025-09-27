@echo off
:: Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment. Please ensure Python is installed.
    pause
    exit /b %errorlevel%
)

:: Activate virtual environment
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b %errorlevel%
)

:: Install requirements
echo Installing requirements...
pip install pywinauto pyautogui
if %errorlevel% neq 0 (
    echo Failed to install requirements. Please check your internet connection or Python setup.
    pause
    exit /b %errorlevel%
)

:: Run the script
echo Running main.py...
python main.py
if %errorlevel% neq 0 (
    echo Failed to run main.py.
    pause
    exit /b %errorlevel%
)

echo Script execution completed.
pause
