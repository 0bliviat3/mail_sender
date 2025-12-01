@echo off
pip install pyinstaller
pyinstaller --onefile --windowed email_sender.py
pyinstaller --onefile --windowed email_sender_advanced.py
echo.
echo Build complete! Check the 'dist' folder.
pause
