import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from pathlib import Path
import json

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("대량 맞춤 메일 발송 프로그램")
        self.root.geometry("900x700")
        
        # 설정 저장용
        self.config_file = "email_config.json"
        self.load_config()
        
        # 수신자 데이터
        self.recipients_data = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 1. 발신자 설정 섹션
        sender_frame = ttk.LabelFrame(main_frame, text="발신자 설정", padding="10")
        sender_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(sender_frame, text="발신 이메일:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.sender_email = ttk.Entry(sender_frame, width=40)
        self.sender_email.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
        self.sender_email.insert(0, self.config.get('sender_email', ''))
        
        ttk.Label(sender_frame, text="비밀번호:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.sender_password = ttk.Entry(sender_frame, width=40, show="*")
        self.sender_password.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        ttk.Label(sender_frame, text="SMTP 서버:").grid(row=2, column=0, sticky=tk.W, pady=2)
        smtp_frame = ttk.Frame(sender_frame)
        smtp_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        self.smtp_server = ttk.Entry(smtp_frame, width=25)
        self.smtp_server.pack(side=tk.LEFT)
        self.smtp_server.insert(0, self.config.get('smtp_server', 'smtp.gmail.com'))
        
        ttk.Label(smtp_frame, text="포트:").pack(side=tk.LEFT, padx=(10, 5))
        self.smtp_port = ttk.Entry(smtp_frame, width=8)
        self.smtp_port.pack(side=tk.LEFT)
        self.smtp_port.insert(0, self.config.get('smtp_port', '587'))
        
        # Gmail 가이드 버튼
        ttk.Button(sender_frame, text="Gmail 설정 가이드", 
                  command=self.show_gmail_guide).grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        # 2. 수신자 데이터 섹션
        recipient_frame = ttk.LabelFrame(main_frame, text="수신자 데이터", padding="10")
        recipient_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(recipient_frame, text="📁 Excel/CSV 파일 불러오기", 
                  command=self.load_recipients).grid(row=0, column=0, pady=5, padx=5)
        
        self.file_label = ttk.Label(recipient_frame, text="파일이 선택되지 않았습니다.", 
                                    foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Button(recipient_frame, text="📋 데이터 미리보기", 
                  command=self.preview_data).grid(row=1, column=0, pady=5, padx=5)
        
        ttk.Button(recipient_frame, text="📝 샘플 파일 생성", 
                  command=self.create_sample_file).grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # 3. 메일 내용 섹션
        content_frame = ttk.LabelFrame(main_frame, text="메일 내용", padding="10")
        content_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        ttk.Label(content_frame, text="메일 제목:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.subject = ttk.Entry(content_frame, width=70)
        self.subject.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        ttk.Label(content_frame, text="메일 본문 템플릿:").grid(row=1, column=0, sticky=(tk.N, tk.W), pady=2)
        ttk.Label(content_frame, text="{{이름}} 을 사용하여 이름을 삽입하세요", 
                 foreground="blue", font=("", 8)).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        self.body_text = scrolledtext.ScrolledText(content_frame, width=70, height=12)
        self.body_text.grid(row=2, column=0, columnspan=2, pady=5, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.body_text.insert(1.0, 
            "안녕하세요, {{이름}}님\n\n"
            "메일 내용을 작성해주세요.\n\n"
            "감사합니다.")
        
        # 4. 전송 옵션 섹션
        option_frame = ttk.LabelFrame(main_frame, text="전송 옵션", padding="10")
        option_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.attach_files = tk.BooleanVar(value=False)
        ttk.Checkbutton(option_frame, text="첨부파일 사용 (Excel 파일에 첨부파일 경로 컬럼 필요)", 
                       variable=self.attach_files).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.test_mode = tk.BooleanVar(value=True)
        ttk.Checkbutton(option_frame, text="테스트 모드 (실제 전송하지 않고 미리보기)", 
                       variable=self.test_mode).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # 5. 전송 버튼 및 상태
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(control_frame, text="✉️  메일 전송 시작", 
                  command=self.send_emails, 
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="💾 설정 저장", 
                  command=self.save_config).pack(side=tk.LEFT, padx=5)
        
        # 6. 로그/상태 표시
        log_frame = ttk.LabelFrame(main_frame, text="전송 로그", padding="5")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=70, height=8, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(5, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(2, weight=1)
        
    def log(self, message):
        """로그 메시지 출력"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update()
        
    def load_recipients(self):
        """수신자 데이터 파일 불러오기"""
        file_path = filedialog.askopenfilename(
            title="수신자 데이터 파일 선택",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            if file_path.endswith('.csv'):
                self.recipients_data = pd.read_csv(file_path, encoding='utf-8-sig')
            else:
                self.recipients_data = pd.read_excel(file_path)
            
            self.file_label.config(
                text=f"✓ {os.path.basename(file_path)} ({len(self.recipients_data)}명)", 
                foreground="green"
            )
            self.log(f"수신자 데이터 로드 완료: {len(self.recipients_data)}명")
            
            # 필수 컬럼 확인
            required_cols = ['이메일', '이름']
            missing_cols = [col for col in required_cols if col not in self.recipients_data.columns]
            if missing_cols:
                messagebox.showwarning("컬럼 확인", 
                    f"필수 컬럼이 없습니다: {', '.join(missing_cols)}\n"
                    f"현재 컬럼: {', '.join(self.recipients_data.columns)}")
        
        except Exception as e:
            messagebox.showerror("오류", f"파일 로드 실패:\n{str(e)}")
            self.log(f"❌ 파일 로드 실패: {str(e)}")
    
    def preview_data(self):
        """데이터 미리보기"""
        if self.recipients_data is None:
            messagebox.showwarning("경고", "먼저 수신자 데이터를 불러와주세요.")
            return
        
        preview_window = tk.Toplevel(self.root)
        preview_window.title("데이터 미리보기")
        preview_window.geometry("800x400")
        
        # 트리뷰 생성
        frame = ttk.Frame(preview_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame, show='headings')
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 컬럼 설정
        tree['columns'] = list(self.recipients_data.columns)
        for col in self.recipients_data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # 데이터 삽입 (최대 100개만)
        for idx, row in self.recipients_data.head(100).iterrows():
            tree.insert('', tk.END, values=list(row))
        
        if len(self.recipients_data) > 100:
            ttk.Label(preview_window, 
                     text=f"※ 처음 100개만 표시됩니다. 전체: {len(self.recipients_data)}개",
                     foreground="blue").pack(pady=5)
    
    def create_sample_file(self):
        """샘플 Excel 파일 생성"""
        sample_data = {
            '이메일': ['user1@example.com', 'user2@example.com', 'user3@example.com'],
            '이름': ['홍길동', '김철수', '이영희'],
            '첨부파일': ['', 'C:/files/document1.pdf', 'C:/files/document2.pdf']
        }
        
        df = pd.DataFrame(sample_data)
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="샘플_수신자_데이터.xlsx"
        )
        
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("완료", f"샘플 파일이 생성되었습니다:\n{file_path}")
            self.log(f"✓ 샘플 파일 생성: {file_path}")
    
    def show_gmail_guide(self):
        """Gmail 설정 가이드 표시"""
        guide = """
Gmail 사용 설정 가이드

1. Gmail 계정에서 2단계 인증 활성화
   - Google 계정 관리 > 보안 > 2단계 인증

2. 앱 비밀번호 생성
   - Google 계정 관리 > 보안 > 앱 비밀번호
   - 앱 선택: 메일
   - 기기 선택: Windows 컴퓨터
   - 생성된 16자리 비밀번호를 복사하여 사용

3. SMTP 설정
   - SMTP 서버: smtp.gmail.com
   - 포트: 587 (TLS) 또는 465 (SSL)

※ 일반 Gmail 비밀번호가 아닌 앱 비밀번호를 사용해야 합니다!
※ 하루 전송 제한: 약 500통 (Gmail 기준)

기타 메일 서비스:
- Naver: smtp.naver.com, 포트 587
- Daum: smtp.daum.net, 포트 465
- Outlook: smtp-mail.outlook.com, 포트 587
        """
        
        messagebox.showinfo("Gmail 설정 가이드", guide)
    
    def send_emails(self):
        """메일 전송 시작"""
        # 유효성 검사
        if not self.sender_email.get():
            messagebox.showwarning("경고", "발신 이메일을 입력해주세요.")
            return
        
        if not self.sender_password.get():
            messagebox.showwarning("경고", "비밀번호를 입력해주세요.")
            return
        
        if self.recipients_data is None:
            messagebox.showwarning("경고", "수신자 데이터를 불러와주세요.")
            return
        
        if not self.subject.get():
            messagebox.showwarning("경고", "메일 제목을 입력해주세요.")
            return
        
        # 확인 대화상자
        if not self.test_mode.get():
            result = messagebox.askyesno(
                "전송 확인",
                f"총 {len(self.recipients_data)}명에게 메일을 전송합니다.\n계속하시겠습니까?"
            )
            if not result:
                return
        
        self.log("=" * 50)
        self.log(f"메일 전송 시작 - {len(self.recipients_data)}명")
        if self.test_mode.get():
            self.log("⚠️ 테스트 모드: 실제 전송되지 않습니다")
        self.log("=" * 50)
        
        success_count = 0
        fail_count = 0
        
        # SMTP 연결 (테스트 모드가 아닐 때만)
        smtp_conn = None
        if not self.test_mode.get():
            try:
                smtp_conn = smtplib.SMTP(self.smtp_server.get(), int(self.smtp_port.get()))
                smtp_conn.starttls()
                smtp_conn.login(self.sender_email.get(), self.sender_password.get())
                self.log("✓ SMTP 서버 연결 성공")
            except Exception as e:
                messagebox.showerror("연결 오류", f"SMTP 서버 연결 실패:\n{str(e)}")
                self.log(f"❌ SMTP 연결 실패: {str(e)}")
                return
        
        # 각 수신자에게 메일 전송
        for idx, row in self.recipients_data.iterrows():
            try:
                recipient_email = row.get('이메일', '')
                recipient_name = row.get('이름', '')
                
                if not recipient_email or pd.isna(recipient_email):
                    self.log(f"⚠️ [{idx+1}] 이메일 주소 없음 - 건너뜀")
                    fail_count += 1
                    continue
                
                # 메일 본문 생성 (이름 치환)
                body = self.body_text.get(1.0, tk.END).strip()
                body = body.replace('{{이름}}', str(recipient_name))
                
                # 메일 메시지 생성
                msg = MIMEMultipart()
                msg['From'] = self.sender_email.get()
                msg['To'] = recipient_email
                msg['Subject'] = self.subject.get()
                
                msg.attach(MIMEText(body, 'plain', 'utf-8'))
                
                # 첨부파일 처리
                if self.attach_files.get() and '첨부파일' in row and row['첨부파일']:
                    attachment_path = row['첨부파일']
                    if not pd.isna(attachment_path) and os.path.exists(attachment_path):
                        try:
                            with open(attachment_path, 'rb') as f:
                                part = MIMEBase('application', 'octet-stream')
                                part.set_payload(f.read())
                                encoders.encode_base64(part)
                                
                                # 파일명을 UTF-8로 인코딩하여 확장자 유지
                                filename = os.path.basename(attachment_path)
                                part.add_header(
                                    'Content-Disposition',
                                    'attachment',
                                    filename=('utf-8', '', filename)
                                )
                                msg.attach(part)
                            self.log(f"  └ 첨부: {os.path.basename(attachment_path)}")
                        except Exception as e:
                            self.log(f"  └ 첨부파일 오류: {str(e)}")
                
                # 전송 (테스트 모드가 아닐 때만)
                if not self.test_mode.get():
                    smtp_conn.send_message(msg)
                    self.log(f"✓ [{idx+1}] {recipient_name} ({recipient_email}) - 전송 완료")
                else:
                    self.log(f"[TEST] [{idx+1}] {recipient_name} ({recipient_email}) - 전송 준비됨")
                
                success_count += 1
                
            except Exception as e:
                self.log(f"❌ [{idx+1}] {recipient_name} - 실패: {str(e)}")
                fail_count += 1
        
        # SMTP 연결 종료
        if smtp_conn:
            smtp_conn.quit()
        
        # 결과 요약
        self.log("=" * 50)
        self.log(f"전송 완료 - 성공: {success_count}, 실패: {fail_count}")
        self.log("=" * 50)
        
        if not self.test_mode.get():
            messagebox.showinfo("완료", 
                f"메일 전송이 완료되었습니다.\n\n"
                f"성공: {success_count}건\n"
                f"실패: {fail_count}건")
        else:
            messagebox.showinfo("테스트 완료", 
                f"테스트 모드 실행 완료\n\n"
                f"전송 준비: {success_count}건\n"
                f"오류: {fail_count}건\n\n"
                f"실제 전송하려면 '테스트 모드'를 해제하세요.")
    
    def save_config(self):
        """설정 저장"""
        config = {
            'sender_email': self.sender_email.get(),
            'smtp_server': self.smtp_server.get(),
            'smtp_port': self.smtp_port.get()
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("저장 완료", "설정이 저장되었습니다.")
            self.log("✓ 설정 저장 완료")
        except Exception as e:
            messagebox.showerror("저장 실패", f"설정 저장 중 오류:\n{str(e)}")
    
    def load_config(self):
        """설정 불러오기"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = {}
        except:
            self.config = {}

def main():
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
