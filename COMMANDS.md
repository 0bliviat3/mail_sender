# PyInstaller EXE 빌드 커맨드 모음

## 🎯 가장 많이 사용하는 커맨드

### 설치
```bash
pip install pyinstaller
```

### 기본 빌드 (콘솔 숨김)
```bash
# 기본 버전
pyinstaller --onefile --windowed --name="메일발송프로그램_기본" email_sender.py

# 고급 버전
pyinstaller --onefile --windowed --name="메일발송프로그램_고급" email_sender_advanced.py
```

### 디버깅용 빌드 (콘솔 보임)
```bash
pyinstaller --onefile --name="메일발송프로그램_기본" email_sender.py
```

### 아이콘 포함 빌드
```bash
pyinstaller --onefile --windowed --icon=icon.ico --name="메일발송프로그램_기본" email_sender.py
```

## 📦 All-in-One 커맨드 (복사해서 사용)

### Windows (CMD/PowerShell)
```cmd
pip install pyinstaller && pyinstaller --onefile --windowed --name="메일발송프로그램_기본" email_sender.py && pyinstaller --onefile --windowed --name="메일발송프로그램_고급" email_sender_advanced.py
```

### Mac/Linux (Terminal)
```bash
pip install pyinstaller && \
pyinstaller --onefile --windowed --name="메일발송프로그램_기본" email_sender.py && \
pyinstaller --onefile --windowed --name="메일발송프로그램_고급" email_sender_advanced.py
```

## 🧹 클린 빌드 (이전 빌드 삭제 후 재빌드)

### Windows
```cmd
rmdir /s /q build dist
del *.spec
pyinstaller --onefile --windowed --name="메일발송프로그램_기본" email_sender.py
```

### Mac/Linux
```bash
rm -rf build dist *.spec
pyinstaller --onefile --windowed --name="메일발송프로그램_기본" email_sender.py
```

## 🎨 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--onefile` | 단일 exe 파일로 생성 |
| `--windowed` | 콘솔 창 숨김 (GUI만) |
| `--name="이름"` | 출력 파일 이름 지정 |
| `--icon=파일.ico` | 아이콘 지정 |
| `--add-data "소스;대상"` | 추가 파일 포함 (Windows) |
| `--add-data "소스:대상"` | 추가 파일 포함 (Mac/Linux) |
| `--exclude-module 모듈` | 특정 모듈 제외 |
| `--upx-dir=경로` | UPX로 압축 |
| `--noconsole` | `--windowed`와 동일 |
| `--debug all` | 디버그 모드 |

## ⚡ 최적화된 빌드

### 최소 크기
```bash
pyinstaller --onefile --windowed \
    --exclude-module matplotlib \
    --exclude-module PIL \
    --exclude-module numpy \
    --name="메일발송프로그램_기본" \
    email_sender.py
```

### UPX 압축 (파일 크기 30-50% 감소)
```bash
# UPX 다운로드 후: https://upx.github.io/
pyinstaller --onefile --windowed --upx-dir=./upx --name="메일발송프로그램_기본" email_sender.py
```

## 🔍 spec 파일 수정 후 재빌드

```bash
# 1. 처음 빌드 (spec 파일 생성됨)
pyinstaller email_sender.py

# 2. email_sender.spec 파일 수정

# 3. spec 파일로 재빌드
pyinstaller email_sender.spec
```

## 🚨 문제 해결 커맨드

### 에러 확인 (콘솔 모드)
```bash
pyinstaller --onefile --name="메일발송프로그램_기본" email_sender.py
```

### 상세 로그 출력
```bash
pyinstaller --onefile --windowed --log-level=DEBUG --name="메일발송프로그램_기본" email_sender.py
```

### 캐시 삭제 후 재빌드
```bash
pyinstaller --clean --onefile --windowed --name="메일발송프로그램_기본" email_sender.py
```

## 📝 빌드 후 확인사항

```bash
# 빌드 결과 확인
dir dist                    # Windows
ls -lh dist                 # Mac/Linux

# 실행 테스트
dist\메일발송프로그램_기본.exe           # Windows
./dist/메일발송프로그램_기본             # Mac/Linux
```

## 💾 배포 파일 압축

### Windows
```cmd
# PowerShell
Compress-Archive -Path dist\*.exe -DestinationPath 메일발송프로그램.zip
```

### Mac/Linux
```bash
cd dist
zip 메일발송프로그램.zip 메일발송프로그램_*
```

## 🎯 완전 자동화 스크립트

### Windows (one-click-build.bat)
```cmd
@echo off
pip install pyinstaller
rmdir /s /q build dist
del *.spec
pyinstaller --onefile --windowed --name="메일발송프로그램_기본" email_sender.py
pyinstaller --onefile --windowed --name="메일발송프로그램_고급" email_sender_advanced.py
echo 빌드 완료! dist 폴더를 확인하세요.
pause
```

### Mac/Linux (one-click-build.sh)
```bash
#!/bin/bash
pip install pyinstaller
rm -rf build dist *.spec
pyinstaller --onefile --windowed --name="메일발송프로그램_기본" email_sender.py
pyinstaller --onefile --windowed --name="메일발송프로그램_고급" email_sender_advanced.py
echo "빌드 완료! dist 폴더를 확인하세요."
```
