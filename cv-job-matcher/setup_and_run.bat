@echo off
cd /d %~dp0

:: Welcome message
echo Welcome to CV Job Matcher setup.
echo This script will install dependencies, download necessary models, and start the Flask server.
echo.

:: Check if Python is installed
echo Checking for Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and add it to your PATH.
    pause
    exit /b 1
)
echo Python found.
echo.

:: Create the data directory if it doesn't exist
echo Ensuring data directory exists...
if not exist "data" mkdir data
echo Data directory ready.
echo.

:: Install required packages
echo Installing required packages from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install packages. Please check requirements.txt and try again.
    pause
    exit /b 1
)
echo Packages installed successfully.
echo.

:: Download spaCy model
echo Downloading spaCy model 'en_core_web_sm'...
python -m spacy download en_core_web_sm
if %errorlevel% neq 0 (
    echo Failed to download spaCy model. Please check your internet connection and try again.
    pause
    exit /b 1
)
echo spaCy model downloaded.
echo.

:: Start the Flask server
echo Starting the Flask server...
python app.py
if %errorlevel% neq 0 (
    echo Failed to start the Flask server. Please check the error messages above.
    pause
    exit /b 1
)