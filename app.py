import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import tempfile
import json

# 從 Streamlit secrets 拿到 service account dict
gcp_service_account_info = st.secrets["gcp_service_account"]

# 把 service account JSON 寫入臨時檔案
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    json.dump(gcp_service_account_info, f)
    temp_cred_path = f.name

# 用臨時 JSON 檔案路徑建立 Firebase 憑證
cred = credentials.Certificate(temp_cred_path)

# 初始化 Firebase app（避免重複初始化）
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# 取得 Firestore 實例
db = firestore.client()

# Streamlit 介面
st.title("Firebase 心情日記")

# 表單區塊
with st.form("diary_form"):
    name = st.text_input("你的名字（可匿名）")
    mood = st.selectbox("今天的心情", ["😊 開心", "😐 普通", "😢 難過", "😠 生氣"])
    message = st.text_area("想說的話")
    submitted = st.form_submit_button("送出")

    if submitted:
        # 將資料寫入 Firestore
        db.collection("diary_entries").add({
            "name": name if name else "匿名",
            "mood": mood,
            "message": message,
        })
        st.success("日記已送出！")

# 顯示最新的 10 筆日記
st.subheader("最新的心情日記")
entries = db.collection("diary_entries").order_by("name").limit(10).stream()

for entry in entries:
    data = entry.to_dict()
    st.markdown(f"**{data['name']}**（{data['mood']}）說：")
    st.write(f"> {data['message']}")
    st.markdown("---")
