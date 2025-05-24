import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json

st.set_page_config(page_title="匿名心情日記牆", layout="centered")
st.title("🧡 匿名心情日記牆")
st.write("在這裡寫下你的心情，我們會幫你記下來。")

# 從 st.secrets 讀取 service account json dict
gcp_sa_info = st.secrets["gcp_service_account"]

# 將 dict 轉成 json 字串，再用 google.oauth 讀取
gcp_sa_json_str = json.dumps(gcp_sa_info)

# 設定授權範圍
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# 建立 Credentials 物件
creds = Credentials.from_service_account_info(json.loads(gcp_sa_json_str), scopes=scope)

# 建立 gspread client
gc = gspread.authorize(creds)

# 開啟 Google Sheet（名稱要跟你自己的試算表一致）
sheet = gc.open("Emotion comment").sheet1

# 使用者輸入區
mood = st.selectbox("請選擇一個心情標籤：", ["😀 開心", "😢 難過", "😡 生氣", "😴 累爆", "🤔 思考中", "🌈 其他"])
message = st.text_area("請輸入你的心情訊息（匿名）：", max_chars=200)

if st.button("送出留言"):
    if message.strip() == "":
        st.warning("請先輸入內容！")
    else:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([now, mood, message])
        st.success("留言成功！")

# 顯示最新留言
st.markdown("---")
st.subheader("🕊 最新 10 則留言")

records = sheet.get_all_records()
df = pd.DataFrame(records)
df = df.tail(10)
df = df[::-1].reset_index(drop=True)

for i, row in df.iterrows():
    st.markdown(f"**{row['timestamp']}** | {row['mood']}")
    st.markdown(f"> {row['message']}")
    st.markdown("---")
