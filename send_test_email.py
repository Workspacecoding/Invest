import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 換成你自己的帳號密碼
EMAIL_ADDRESS = "milai8899@gmail.com"
EMAIL_PASSWORD = "lhni syxg dukj advv"
TO_EMAIL = "workspacecloud0@gmail.com"  # 寄給誰，也可以設成自己測試

# 建立郵件內容
msg = MIMEMultipart()
msg["From"] = EMAIL_ADDRESS
msg["To"] = TO_EMAIL
msg["Subject"] = "這是測試信件 ✉️"

body = "這是一封測試用的自動寄送 email，確認 SMTP 設定是否正常～"
msg.attach(MIMEText(body, "plain"))

# 使用 Gmail 的 SMTP 發信
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print("✅ 測試信件已成功寄出！請去收件匣看看吧～")
except Exception as e:
    print("❌ 發信失敗：", e)
