@echo off
echo Installing pip and dependencies for Pomodoro timer application...
echo.

REM Download and install pip if not already installed
python -m ensurepip --default-pip

REM Install dependencies with pip
python -m pip install pillow


echo.
echo Pip and dependencies have been installed successfully.
echo.
pause
