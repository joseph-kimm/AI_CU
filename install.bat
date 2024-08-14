@echo off

REM Download Python installer
curl -o python-3.11.9-amd64.exe https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

REM Install Python
python-3.11.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

REM Create a virtual environment
py -m venv ai_cu_env

REM Activate the virtual environment
ai_cu_env\Scripts\activate

REM Upgrade pip
py -m pip install --upgrade pip

REM Download Dlib
curl -o dlib-19.24.1-cp311-cp311-win_amd64.whl https://github.com/z-mahmud22/Dlib_Windows_Python3.x/blob/main/dlib-19.24.1-cp311-cp311-win_amd64.whl

REM Install Dlib
pip install dlib-19.24.1-cp311-cp311-win_amd64.whl

REM Install required libraries
pip install -r requirements.txt

REM Cleanup
del python-3.11.9-amd64.exe

echo Installation complete.
pause
