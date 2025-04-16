
import pandas as pd
import yfinance as yf
import smtplib
import schedule
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === 參數設定 ===
YOUR_EMAIL = "milai8899@gmail.com"          # 寄件者 Gmail
YOUR_PASSWORD = "lhni syxg dukj advv"          # Gmail 應用程式密碼
TO_EMAIL = "workspacecloud0@gmail.com"      # 收件者 Email

# === 發送 Email 函式 ===
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = YOUR_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(YOUR_EMAIL, YOUR_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

# === 抓資料 ===
def fetch_data():
    nasdaq = yf.download("^IXIC", period="5d", interval="1d")["Close"][-1]
    usdtwd = yf.download("TWD=X", period="5d", interval="1d")["Close"][-1]
    us10y = yf.download("^TNX", period="5d", interval="1d")["Close"][-1] / 10
    return nasdaq, usdtwd, us10y

# === 分析邏輯 ===
def analyze(nasdaq, usdtwd, us10y):
    suggestion = ""
    if nasdaq > 15000 and usdtwd < 32.5 and us10y < 3.5:
        suggestion = "積極買進 (強烈利多)"
    elif nasdaq > 15000 and usdtwd < 33.5 and us10y < 4:
        suggestion = "小量佈局"
    elif usdtwd > 33.5 and us10y > 4:
        suggestion = "觀望：資金成本高、美元偏貴"
    else:
        suggestion = "觀望：訊號不明確"
    return suggestion

# === 主程式 ===
def job():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nasdaq, usdtwd, us10y = fetch_data()
    decision = analyze(nasdaq, usdtwd, us10y)

    body = f"Date: {now}\n" \
           f"NASDAQ: {nasdaq:,.2f}\n" \
           f"USD/TWD: {usdtwd:.2f}\n" \
           f"US10Y Yield: {us10y:.2f}%\n\n" \
           f"Suggested Action: {decision}"

    send_email("Daily Investment Alert", body)

# 安排每天 9:00 執行
schedule.every().day.at("09:00").do(job)

print("開始監控，將於每天早上 9:00 發送通知 Email")
while True:
    schedule.run_pending()
    time.sleep(30)
