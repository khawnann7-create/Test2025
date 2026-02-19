import streamlit as st
import requests
import random
import time

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Netflix 2025 Pro", layout="wide")

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# -------------------------
# 🎨 Netflix Style
# -------------------------
st.markdown("""
<style>
.stApp {
    background-color: #141414;
    color: white;
}

.sidebar .sidebar-content {
    background-color: #000000;
}

.title {
    font-size: 40px;
    font-weight: bold;
    color: #E50914;
}

.movie-card {
    transition: transform 0.3s;
}
.movie-card:hover {
    transform: scale(1.1);
}

.top10 {
    font-size: 22px;
    font-weight: bold;
    color: #E50914;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 📥 ดึงข้อมูลหนังปี 2025
# -------------------------
@st.cache_data
def get_movies():
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "primary_release_year": 2025,
        "sort_by": "popularity.desc"
    }
    res = requests.get(url, params=params)
    return res.json().get("results", [])

movies = get_movies()

# -------------------------
# 🎯 SIDEBAR MENU
# -------------------------
st.sidebar.title("🎬 MENU")

menu = st.sidebar.radio(
    "เลือกเมนู",
    ["🏠 หน้าแรก", "🔥 Top 10", "🎲 สุ่มตามแนว"]
)

# -------------------------
# 🏠 หน้าแรก
# -------------------------
if menu == "🏠 หน้าแรก":
    st.markdown('<div class="title">NETFLIX 2025</div>', unsafe_allow_html=True)
    st.write("หนังยอดนิยมปี 2025 (ข้อมูลจริงจาก TMDB)")

    cols = st.columns(5)
    for col, movie in zip(cols, movies[:5]):
        with col:
            poster = IMAGE_BASE + movie["poster_path"] if movie["poster_path"] else ""
            st.image(poster)
            st.caption(movie["title"])

# -------------------------
# 🔥 TOP 10
# -------------------------
elif menu == "🔥 Top 10":
    st.markdown('<div class="title">TOP 10 MOVIES 2025</div>', unsafe_allow_html=True)

    for i, movie in enumerate(movies[:10], start=1):
        poster = IMAGE_BASE + movie["poster_path"]
        col1, col2 = st.columns([1,3])

        with col1:
            st.image(poster)

        with col2:
            st.markdown(f'<div class="top10">#{i} {movie["title"]}</div>', unsafe_allow_html=True)
            st.write("⭐ คะแนน:", movie["vote_average"])
            st.write("📅 วันที่ฉาย:", movie["release_date"])
            st.write("📝", movie["overview"])

        st.markdown("---")

# -------------------------
# 🎲 สุ่มตามแนว
# -------------------------
elif menu == "🎲 สุ่มตามแนว":
    st.markdown('<div class="title">สุ่มหนังตามแนว</div>', unsafe_allow_html=True)

    # ดึง Genre
    genre_url = f"{BASE_URL}/genre/movie/list"
    genre_res = requests.get(genre_url, params={"api_key": API_KEY})
    genres = genre_res.json()["genres"]

    genre_dict = {g["name"]: g["id"] for g in genres}
    selected_genre = st.selectbox("เลือกแนวหนัง", list(genre_dict.keys()))

    if st.button("🎰 สุ่มเลย!"):
        with st.spinner("กำลังสุ่มหนังให้คุณ... 🎬"):
            time.sleep(2)

            discover_url = f"{BASE_URL}/discover/movie"
            params = {
                "api_key": API_KEY,
                "primary_release_year": 2025,
                "with_genres": genre_dict[selected_genre]
            }
            res = requests.get(discover_url, params=params)
            results = res.json().get("results", [])

            if results:
                movie = random.choice(results)
                poster = IMAGE_BASE + movie["poster_path"]

                st.image(poster, width=300)
                st.success(f"🎬 {movie['title']}")
                st.write("⭐ คะแนน:", movie["vote_average"])
                st.write("📅 วันที่ฉาย:", movie["release_date"])
                st.write("📝", movie["overview"])
            else:
                st.warning("ไม่พบหนังในแนวนี้")
