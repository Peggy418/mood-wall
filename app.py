from io import StringIO
import os, json
key_str = os.environ["your_key"]
key_dict = json.loads(key_str)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd

# ===== 1. Google Sheets API 連線設定 =====
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("your_key.json", scope)
gc = gspread.authorize(credentials)

# 📝 換成你的 Google Sheet 名稱
sheet = gc.open("Emotion comment").sheet1

# ===== 2. Streamlit 畫面設定 =====
st.set_page_config(page_title="匿名心情日記牆", layout="centered")
st.title("🧡 匿名心情日記牆")
st.write("在這裡寫下你的心情，我們會幫你記下來。")

# ===== 3. 使用者輸入區 =====
mood = st.selectbox("請選擇一個心情標籤：", ["😀 開心", "😢 難過", "😡 生氣", "😴 累爆", "🤔 思考中", "🌈 其他"])
message = st.text_area("請輸入你的心情訊息（匿名）：", max_chars=200)

if st.button("送出留言"):
    if message.strip() == "":
        st.warning("請先輸入內容！")
    else:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([now, mood, message])
        st.success("留言成功！")

# ===== 4. 顯示最新留言 =====
st.markdown("---")
st.subheader("🕊 最新 10 則留言")

# 讀取資料
records = sheet.get_all_records()
df = pd.DataFrame(records)
df = df.tail(10)  # 取最後10筆

# 反向排序（最新在上面）
df = df[::-1].reset_index(drop=True)

for i, row in df.iterrows():
    st.markdown(f"**{row['timestamp']}** | {row['mood']}")
    st.markdown(f"> {row['message']}")
    st.markdown("---")
