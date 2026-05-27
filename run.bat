@echo off
REM MarkItDown GUI Launcher
REM Simply double-click this file to start the converter

echo Starting MarkItDown GUI...
python gui_harness.py
if errorlevel 1 (
    echo Error running MarkItDown. Please ensure Python is installed.
    pause
)
