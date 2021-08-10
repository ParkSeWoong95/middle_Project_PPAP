import smtplib                              # 메일을 보내기 위한 SMTP 모듈
from email.mime.text import MIMEText

class MyMail:
    def mysendmail(self,recvEmail, title, content):
        smtpName = "smtp.naver.com"                  # smtp 서버 주소
        smtpPort = 587                               # smtp 포트 번호
        
        sendEmail = "rookoo8904@naver.com"
        password = "tmp202012M!!"
                                    
        msg = MIMEText(content)                       # MIMEText(text , _charset = "utf8")
        msg['From'] = sendEmail
        msg['To'] = recvEmail
        msg['Subject'] = title
        
        print(msg.as_string())                        
        
        s = smtplib.SMTP(smtpName , smtpPort)         # 메일 서버 연결
        s.starttls()                                  # TLS 보안 처리
        s.login(sendEmail , password)                 # 로그인
        s.sendmail(sendEmail, recvEmail, msg.as_string())  # 메일 전송, 문자열로 변환하여 보냅니다.
        s.close()                                     # smtp 서버 연결을 종료합니다.

if __name__ == '__main__':
    pass
#     content = "메일 테스트"
#     email = "asvsasdfjx11231hd@naver.com"
#     MyMail().mysendmail(email, "메일 테스트", content)