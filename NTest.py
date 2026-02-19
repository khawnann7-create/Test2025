import streamlit as st
import pandas as pd

# ----------------------------
# ตั้งค่าหน้าเว็บ
# ----------------------------
st.set_page_config(
    page_title="Movies 2025 Recommender",
    layout="wide"
)

# ----------------------------
# ธีมสไตล์ Netflix
# ----------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #141414;
        color: white;
    }

    .main-title {
        font-size: 45px;
        font-weight: bold;
        color: #E50914;
    }

    .movie-box {
        background-color: #1f1f1f;
        padding: 20px;
        border-radius: 15px;
        margin-top: 15px;
    }

    .rating {
        color: #E50914;
        font-weight: bold;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# หัวข้อ
# ----------------------------
st.markdown('<div class="main-title">🎬 MOVIES 2025</div>', unsafe_allow_html=True)
st.write("ระบบแสดงหนังปี 2025 และสุ่มแนะนำอัตโนมัติ")

# ----------------------------
# ข้อมูลหนังปี 2025
# ----------------------------
data = {
    "ชื่อหนัง": [
        "Captain America: Brave New World",
        "Deadpool 3",
        "Mission: Impossible 8",
        "Snow White (Live Action)",
        "Avatar 3",
        "The Batman Part II",
        "Inside Out 2",
        "Joker: Folie à Deux",
        "Fast & Furious 11",
        "Thunderbolts"
    ],
    "ประเภท": [
        "Action", "Action", "Action", "Fantasy", "Sci-Fi",
        "Action", "Animation", "Drama", "Action", "Action"
    ],
    "ปี": [2025]*10,
    "คะแนนคาดการณ์": [8.5, 8.8, 8.2, 7.5, 9.0, 8.7, 8.0, 8.4, 7.9, 8.1]
}

df = pd.DataFrame(data)

# ----------------------------
# แสดงตารางหนังทั้งหมด
# ----------------------------
st.subheader("📋 รายชื่อหนังทั้งหมดปี 2025")
st.dataframe(df, use_container_width=True)

# ----------------------------
# ปุ่มสุ่มแนะนำ
# ----------------------------
st.markdown("---")
st.subheader("🎲 สุ่มแนะนำหนัง")

if st.button("สุ่มแนะนำหนังให้ฉัน 🎬"):
    random_movie = df.sample(1).iloc[0]

    st.markdown('<div class="movie-box">', unsafe_allow_html=True)
    st.success("🔥 เราแนะนำเรื่องนี้ให้คุณ")

    st.write("🎬 ชื่อเรื่อง:", random_movie["ชื่อหนัง"])
    st.write("🎭 ประเภท:", random_movie["ประเภท"])
    st.write("📅 ปี:", random_movie["ปี"])
    st.markdown(
        f'<div class="rating">⭐ คะแนนคาดการณ์: {random_movie["คะแนนคาดการณ์"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)
