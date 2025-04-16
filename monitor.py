import pandas as pd
import yfinance as yf
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

YOUR_EMAIL = "milai8899@gmail.com"
YOUR_PASSWORD = "lhni syxg dukj advv"
TO_EMAIL = "workspacecloud0@gmail.com"

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
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)

def fetch_data():
    print("📊 Fetching data...")
    nasdaq = yf.download("^IXIC", period="5d", interval="1d")["Close"][-1]
    usdtwd = yf.download("TWD=X", period="5d", interval="1d")["Close"][-1]
    us10y = yf.download("^TNX", period="5d", interval="1d")["Close"][-1] / 10
    print(f"📈 NASDAQ: {nasdaq:.2f}, USD/TWD: {usdtwd:.2f}, US10Y: {us10y:.2f}")
    return nasdaq, usdtwd, us10y

def analyze(nasdaq, usdtwd, us10y):
    if nasdaq > 15000 and usdtwd < 32.5 and us10y < 3.5:
        return "積極買進 (強烈利多)"
    elif nasdaq > 15000 and usdtwd < 33.5 and us10y < 4:
        return "小量佈局"
    elif usdtwd > 33.5 and us10y > 4:
        return "觀望：資金成本高、美元偏貴"
    else:
        return "觀望：訊號不明確"

def job():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nasdaq, usdtwd, us10y = fetch_data()
    decision = analyze(nasdaq, usdtwd, us10y)
    body = f"🗓️ Date: {now}\n" \
           f"NASDAQ: {nasdaq:,.2f}\n" \
           f"USD/TWD: {usdtwd:.2f}\n" \
           f"US10Y Yield: {us10y:.2f}%\n\n" \
           f"📌 Suggested Action: {decision}"
    print("📬 Sending email...")
    send_email("Daily Investment Alert", body)

# 👉 執行一次
print("🚀 開始執行投資監控任務")
job()
