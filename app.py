import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime
import pandas as pd

# 設定 Google API 權限範圍
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# 從 secrets 讀取服務帳號資訊並授權
creds = Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=scope)
gc = gspread.authorize(creds)

# 開啟 Google Sheet
sheet = gc.open("Emotion comment").sheet1

# 讀取所有留言
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Streamlit UI
st.title("🧡 匿名心情日記牆")

mood = st.selectbox("請選擇一個心情標籤：", ["😀 開心", "😢 難過", "😡 生氣", "😴 累爆", "🤔 思考中", "🌈 其他"])
message = st.text_area("請輸入你的心情訊息（匿名）：", max_chars=200)

if st.button("送出留言"):
    if message.strip() == "":
        st.warning("請先輸入內容！")
    else:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([now, mood, message])
        st.success("留言成功！")

        # 重新載入留言資料
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

# 顯示留言牆
for i, row in df.iterrows():
    st.markdown(f"**{row['timestamp']}** | {row['mood']}")
    st.markdown(f"> {row['message']}")
    st.markdown("---")


