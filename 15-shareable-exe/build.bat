@echo off
REM Build TeamBot.exe - double-click this file or run it from a terminal.
python -m pip install -r requirements.txt
python build.py
pause
