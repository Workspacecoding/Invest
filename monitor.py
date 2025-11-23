import pandas as pd
import yfinance as yf
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === 設定 Gmail 帳號與密碼 ===
YOUR_EMAIL = "milai8899@gmail.com"
YOUR_PASSWORD = "lhni syxg dukj advv"
TO_EMAIL = ["workspacecloud0@gmail.com", "beisintw@gmail.com"]

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
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)

# === 抓資料 ===
def fetch_data():
    print("📊 Fetching data...")

    nasdaq_df = yf.download("^IXIC", period="5d", interval="1d")
    usdtwd_df = yf.download("TWD=X", period="5d", interval="1d")
    us10y_df = yf.download("^TNX", period="5d", interval="1d")

    # Debug 用：檢查欄位和資料筆數
    print("NASDAQ 資料筆數：", len(nasdaq_df))
    print("NASDAQ 欄位：", nasdaq_df.columns.tolist())

    # 防呆
    if nasdaq_df.empty or usdtwd_df.empty or us10y_df.empty:
        raise Exception("❌ 無法取得資料")

    try:
        nasdaq = float(nasdaq_df["Close"].iloc[-1])
        usdtwd = float(usdtwd_df["Close"].iloc[-1])
        us10y = float(us10y_df["Close"].iloc[-1]) / 10
    except Exception as e:
        raise Exception(f"❌ 資料轉換失敗: {e}")

    print(f"📈 NASDAQ: {nasdaq:.2f}, USD/TWD: {usdtwd:.2f}, US10Y: {us10y:.2f}")
    return nasdaq, usdtwd, us10y


# === 判斷邏輯 ===
def analyze(nasdaq, usdtwd, us10y):
    if nasdaq > 15000 and usdtwd < 32.5 and us10y < 3.5:
        return "🚀 積極買進（強烈利多）"
    elif nasdaq > 15000 and usdtwd < 33.5 and us10y < 4:
        return "🟢 小量佈局（條件尚可）"
    elif usdtwd > 33.5 and us10y > 4:
        return "🔴 觀望：資金成本高＋美元偏貴"
    else:
        return "🟡 觀望：訊號不明確，等待更佳時機"

# === 主任務 ===
def job():
    print("🚀 開始執行投資監控任務")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        nasdaq, usdtwd, us10y = fetch_data()
        decision = analyze(nasdaq, usdtwd, us10y)

        body = (
            f"📅 日期：{now}\n"
            f"📊 指數與利率狀況：\n"
            f"   - NASDAQ：{nasdaq:,.2f}\n"
            f"   - USD/TWD 匯率：{usdtwd:.2f}\n"
            f"   - 美國 10 年期債券殖利率：{us10y:.2f}%\n\n"
            f"📌 建議操作：{decision}"
        )

        subject = f"📈 每日投資監控通知 | {now.split()[0]}"
        send_email(subject, body)

    except Exception as e:
        print("❌ 發生錯誤：", e)

# === 執行 ===
if __name__ == "__main__":
    job()
