import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. 設定 Google Sheets API 認證範圍
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 2. 從 Streamlit Secrets 讀取憑證 JSON (需先在 Streamlit Cloud 設定 secrets)
creds_dict = st.secrets["gcp"]

# 3. 產生憑證並授權
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# 4. 打開 Google 試算表（請確認試算表名稱和 Service Account 有分享權限）
sheet = client.open("匿名心情日記牆").sheet1

# 5. 設定 Streamlit 網頁標題
st.set_page_config(page_title="匿名心情日記牆")
st.title("🧠 匿名心情日記牆")

# 6. 建立表單讓使用者輸入心情與選擇心情 Emoji
with st.form("mood_form"):
    mood_text = st.text_area("請輸入今天的心情：", height=150)
    emoji = st.selectbox("選擇一個代表今天的心情 Emoji：", ["😊", "😢", "😡", "😴", "❤️", "🥲"])
    submitted = st.form_submit_button("送出")

    if submitted:
        if mood_text.strip() == "":
            st.warning("請輸入一些內容！")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 新增一列，放在第2行（表頭後面）
            sheet.insert_row([mood_text, emoji, now], 2)
            st.success("你的心情已成功送出！")

# 7. 顯示最新10筆心情留言
st.subheader("💬 最新心情留言")
records = sheet.get_all_records()
latest = records[:10]

for row in latest:
    st.markdown(f"{row['Emoji']} **{row['心情內容']}**")
    st.caption(f"🕒 {row['時間']}")
    st.markdown("---")
