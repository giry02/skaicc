@echo off
setlocal

:: Check if python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [Error] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    goto :end
)

:: Install dependencies
echo Installing dependencies...
python -m pip install openai python-pptx pillow colorama python-dotenv
if %errorlevel% neq 0 (
    echo [Error] Failed to install dependencies.
    goto :end
)

:: Run integrity check
echo Checking file integrity...
python check_integrity.py

:: Run analysis
echo Running comprehensive analysis...
python analyze_all.py
if %errorlevel% neq 0 (
    echo [Error] Analysis script failed.
    goto :end
)

echo.
echo Analysis complete!
echo output: project_context.txt and comprehensive_analysis.md

:end
pause
