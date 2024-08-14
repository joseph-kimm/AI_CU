@echo off

REM Specify the desired Python version
set PYTHON_VERSION=3.11

REM Download Python installer
curl -o python-installer.exe https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

REM Install Python
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Cleanup
del python-installer.exe

echo Installation complete.
pause