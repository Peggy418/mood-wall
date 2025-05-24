import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ✅ 1. 從 secrets 讀取 Google Sheets API 憑證
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["gcp"]  # 👈 從 Streamlit secrets 讀取
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(creds)
sheet = client.open("匿名心情日記牆").sheet1

# ✅ 2. UI 顯示
st.set_page_config(page_title="匿名心情日記牆")
st.title("🧠 匿名心情日記牆")

with st.form("mood_form"):
    mood_text = st.text_area("請輸入今天的心情：", height=150)
    emoji = st.selectbox("選擇一個代表今天的心情 Emoji：", ["😊", "😢", "😡", "😴", "❤️", "🥲"])
    submitted = st.form_submit_button("送出")

    if submitted:
        if mood_text.strip() == "":
            st.warning("請輸入一些內容！")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.insert_row([mood_text, emoji, now], 2)
            st.success("你的心情已成功送出！")

# ✅ 3. 顯示最新 10 筆留言
st.subheader("💬 最新心情留言")
records = sheet.get_all_records()
latest = records[:10]

for row in latest:
    st.markdown(f"{row['Emoji']} **{row['心情內容']}**")
    st.caption(f"🕒 {row['時間']}")
    st.markdown("---")

