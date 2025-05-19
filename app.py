import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import os, json

===== 1. Google Sheets API 金鑰設定（從 Secrets） =====
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
key_str = os.environ["your_key"] # ← 這裡從 Streamlit Secrets 讀取
key_dict = json.loads(key_str)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
gc = gspread.authorize(credentials)

===== 2. 連接 Google Sheet =====
sheet = gc.open("Emotion comment").sheet1 # ← 換成你的試算表名稱

===== 3. Streamlit 畫面設定 =====
st.set_page_config(page_title="匿名心情日記牆", layout="centered")
st.title("🧡 匿名心情日記牆")
st.write("在這裡寫下你的心情，我們會幫你記下來。")

===== 4. 使用者輸入區 =====
mood = st.selectbox("請選擇一個心情標籤：", ["😀 開心", "😢 難過", "😡 生氣", "😴 累爆", "🤔 思考中", "🌈 其他"])
message = st.text_area("請輸入你的心情訊息（匿名）：", max_chars=200)

if st.button("送出留言"):
if message.strip() == "":
st.warning("請先輸入內容！")
else:
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sheet.append_row([now, mood, message])
st.success("留言成功！")

===== 5. 顯示最新留言 =====
st.markdown("---")
st.subheader("🕊 最新 10 則留言")

records = sheet.get_all_records()
df = pd.DataFrame(records)
df = df.tail(10)[::-1].reset_index(drop=True) # 最新的在最上面

for i, row in df.iterrows():
st.markdown(f"📅 {row['timestamp']} | {row['mood']}")
st.markdown(f"> {row['message']}")
st.markdown("---")
