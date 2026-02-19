import streamlit as st
import requests
import random

# ----------------------------
# ตั้งค่า
# ----------------------------
st.set_page_config(page_title="Netflix 2025", layout="wide")

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# ----------------------------
# 🎨 Netflix Style
# ----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #141414;
    color: white;
}

.title {
    font-size: 45px;
    font-weight: bold;
    color: #E50914;
}

.scroll-container {
    display: flex;
    overflow-x: auto;
    gap: 20px;
    padding: 10px;
}

.movie-card {
    min-width: 200px;
    transition: transform 0.3s;
}

.movie-card:hover {
    transform: scale(1.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">NETFLIX 2025</div>', unsafe_allow_html=True)
st.write("หนังปี 2025 ดึงข้อมูลจริงจาก TMDB")

# ----------------------------
# ดึงหนังปี 2025
# ----------------------------
def get_movies_2025():
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "primary_release_year": 2025,
        "sort_by": "popularity.desc"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("results", [])

movies = get_movies_2025()

# ----------------------------
# 🔥 แสดงแบบเลื่อนแนวนอน
# ----------------------------
st.subheader("🔥 หนังยอดนิยมปี 2025")

if movies:
    html = '<div class="scroll-container">'
    for movie in movies[:15]:
        poster = IMAGE_BASE + movie["poster_path"] if movie["poster_path"] else ""
        html += f"""
            <div class="movie-card">
                <img src="{poster}" width="200">
                <p>{movie['title']}</p>
            </div>
        """
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)
else:
    st.error("ไม่สามารถดึงข้อมูลหนังได้")

# ----------------------------
# 🎲 สุ่มแนะนำ
# ----------------------------
st.markdown("---")
st.subheader("🎲 สุ่มแนะนำหนังปี 2025")

if st.button("สุ่มแนะนำให้ฉัน 🎬"):
    if movies:
        movie = random.choice(movies)
        poster = IMAGE_BASE + movie["poster_path"]

        st.image(poster, width=300)
        st.success(f"🎬 {movie['title']}")
        st.write("⭐ คะแนน:", movie["vote_average"])
        st.write("📅 วันเข้าฉาย:", movie["release_date"])
        st.write("📝 เรื่องย่อ:", movie["overview"])
    else:
        st.warning("ไม่มีข้อมูลหนัง")
