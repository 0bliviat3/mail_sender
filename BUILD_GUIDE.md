# EXE 파일 빌드 가이드

## 🚀 빠른 빌드 (자동)

### Windows 사용자
```cmd
build_exe.bat
```
더블클릭으로 실행하거나 명령 프롬프트에서 실행하세요.

### Mac/Linux 사용자
```bash
chmod +x build_exe.sh
./build_exe.sh
```

## 📝 수동 빌드 (단계별)

### 1단계: PyInstaller 설치
```bash
pip install pyinstaller
```

### 2단계: 기본 버전 빌드
```bash
pyinstaller --onefile --windowed --name="메일발송프로그램_기본" email_sender.py
```

### 3단계: 고급 버전 빌드
```bash
pyinstaller --onefile --windowed --name="메일발송프로그램_고급" email_sender_advanced.py
```

## 📦 빌드 옵션 설명

### 기본 옵션
- `--onefile`: 단일 실행 파일로 생성
- `--windowed`: 콘솔 창 숨김 (GUI만 표시)
- `--name="이름"`: 생성될 exe 파일 이름

### 추가 옵션 (선택사항)

#### 아이콘 추가
```bash
pyinstaller --onefile --windowed --icon=email_icon.ico --name="메일발송프로그램_기본" email_sender.py
```
※ email_icon.ico 파일이 있어야 합니다

#### 콘솔 창 보이기 (디버깅용)
```bash
pyinstaller --onefile --name="메일발송프로그램_기본" email_sender.py
```
※ `--windowed` 제거

#### 파일 크기 최적화
```bash
pyinstaller --onefile --windowed --name="메일발송프로그램_기본" --exclude-module matplotlib --exclude-module PIL email_sender.py
```

## 📂 빌드 결과

빌드 완료 후 생성되는 폴더:
```
프로젝트폴더/
├── build/              # 빌드 중간 파일 (삭제 가능)
├── dist/               # 최종 실행 파일 위치 ★
│   ├── 메일발송프로그램_기본.exe
│   └── 메일발송프로그램_고급.exe
├── email_sender.spec   # 빌드 설정 파일
└── email_sender_advanced.spec
```

**중요**: `dist` 폴더 안의 exe 파일만 배포하면 됩니다!

## 🎯 배포용 패키징

### 옵션 1: EXE만 배포
```
메일발송프로그램_기본.exe  (약 15-20MB)
메일발송프로그램_고급.exe  (약 15-20MB)
```
- 장점: 간단함
- 단점: 사용자가 README를 못 볼 수 있음

### 옵션 2: 폴더로 배포 (추천)
```
메일발송프로그램/
├── 메일발송프로그램_기본.exe
├── 메일발송프로그램_고급.exe
├── README.md
├── QUICKSTART.md
└── 샘플_수신자_데이터.xlsx
```

폴더를 zip으로 압축하여 배포

## ⚠️ 주의사항

### 1. 바이러스 경고
- PyInstaller로 만든 exe는 일부 백신에서 오탐지될 수 있음
- 해결방법:
  - 백신 예외 목록에 추가
  - 코드 서명 인증서 구매 (유료)
  - VirusTotal에서 검사 후 안전함을 증명

### 2. Windows Defender
- 처음 실행 시 "Windows의 PC 보호" 경고 나올 수 있음
- "추가 정보" → "실행" 클릭

### 3. 파일 크기
- 단일 exe 파일 크기: 약 15-20MB
- Python 인터프리터와 모든 라이브러리 포함됨
- 정상적인 크기입니다

### 4. 실행 속도
- 첫 실행이 조금 느릴 수 있음 (압축 해제 때문)
- 두 번째부터는 빠름

## 🔧 고급 빌드 옵션

### UPX로 파일 크기 줄이기
```bash
# UPX 다운로드: https://upx.github.io/
pyinstaller --onefile --windowed --upx-dir=C:/upx --name="메일발송프로그램_기본" email_sender.py
```
약 30-50% 크기 감소

### 버전 정보 추가 (Windows)
```bash
# version_info.txt 생성 후
pyinstaller --onefile --windowed --version-file=version_info.txt --name="메일발송프로그램_기본" email_sender.py
```

### spec 파일 사용 (재빌드 시 편리)
```bash
# 첫 빌드
pyinstaller email_sender.py

# spec 파일 수정 후 재빌드
pyinstaller email_sender.spec
```

## 🐛 문제 해결

### "Failed to execute script" 오류
```bash
# --windowed 제거하여 에러 메시지 확인
pyinstaller --onefile --name="메일발송프로그램_기본" email_sender.py
```

### "No module named 'pandas'" 오류
```bash
# 가상환경이 아닌 시스템 Python 사용
# 또는 spec 파일에 hiddenimports 추가
hiddenimports=['pandas', 'openpyxl']
```

### 실행 파일이 너무 큼
```bash
# 불필요한 모듈 제외
pyinstaller --onefile --windowed --exclude-module matplotlib --exclude-module numpy email_sender.py
```

### 한글 파일명 문제
- 빌드 명령에서 영문 이름 사용:
```bash
pyinstaller --onefile --windowed --name="EmailSender" email_sender.py
```
- 빌드 후 파일명 변경

## 📋 빌드 체크리스트

빌드 전:
- [ ] 모든 기능이 Python 스크립트에서 정상 작동하는지 확인
- [ ] requirements.txt의 모든 패키지 설치 확인
- [ ] 테스트 모드로 실행 테스트

빌드 중:
- [ ] PyInstaller 최신 버전 사용
- [ ] 콘솔 에러 메시지 확인

빌드 후:
- [ ] dist 폴더의 exe 파일 실행 테스트
- [ ] 다른 컴퓨터에서도 실행 테스트
- [ ] 바이러스 검사 (VirusTotal)

## 💡 팁

### 빠른 재빌드
```bash
# build, dist 폴더 삭제 후 재빌드
rmdir /s /q build dist
pyinstaller --onefile --windowed --name="메일발송프로그램_기본" email_sender.py
```

### 개발 중에는 Python으로
개발/테스트: `python email_sender.py`
최종 배포: `pyinstaller`로 exe 생성

### 자동 업데이트 기능
코드에 버전 체크 기능 추가하여 새 버전 알림 가능

## 📞 도움이 필요하면

1. PyInstaller 공식 문서: https://pyinstaller.org/
2. 에러 메시지를 구글에 검색
3. 콘솔 모드로 실행하여 정확한 에러 확인
