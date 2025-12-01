@echo off
echo ================================================
echo 대량 메일 발송 프로그램 EXE 빌드 스크립트
echo ================================================
echo.

echo [1/4] PyInstaller 설치 중...
pip install pyinstaller
echo.

echo [2/4] 기본 버전 빌드 중...
pyinstaller --onefile --windowed --icon=NONE ^
    --name="email_sender" ^
    --add-data "email_config.json;." ^
    email_sender.py
echo.

echo [3/4] 고급 버전 빌드 중...
pyinstaller --onefile --windowed --icon=NONE ^
    --name="email_sender_advanced" ^
    --add-data "email_config.json;." ^
    email_sender_advanced.py
echo.

echo [4/4] 빌드 완료!
echo.
echo ================================================
echo EXE 파일 위치:
echo - dist\email_sender.exe
echo - dist\email_sender_advanced.exe
echo ================================================
echo.
pause
