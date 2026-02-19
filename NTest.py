import streamlit as st
import requests
import random

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Netflix Pro 2025", layout="wide")

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# -----------------------------
# SESSION STATE
# -----------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "watchlist" not in st.session_state:
    st.session_state.watchlist = {}

# -----------------------------
# 🎨 STYLE
# -----------------------------
st.markdown("""
<style>
.stApp { background-color: #141414; color: white; }
.title { font-size:40px; color:#E50914; font-weight:bold; }
.card { background:#1f1f1f; padding:10px; border-radius:15px; }
.watch-btn { background:#E50914; color:white; padding:5px 10px; border-radius:8px; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🔐 LOGIN SYSTEM
# -----------------------------
def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.user = username
            if username not in st.session_state.watchlist:
                st.session_state.watchlist[username] = []
            st.success("Login สำเร็จ!")
            st.rerun()
        else:
            st.error("กรอกข้อมูลให้ครบ")

if not st.session_state.user:
    login()
    st.stop()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title(f"👤 {st.session_state.user}")
menu = st.sidebar.radio("Menu", ["🏠 Home", "🔥 Top 10", "❤️ My Watchlist", "🚪 Logout"])

if menu == "🚪 Logout":
    st.session_state.user = None
    st.rerun()

# -----------------------------
# 📥 ดึงหนังปี 2025
# -----------------------------
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

# -----------------------------
# 🏠 HOME
# -----------------------------
if menu == "🏠 Home":
    st.markdown('<div class="title">Movies 2025</div>', unsafe_allow_html=True)

    cols = st.columns(4)

    for col, movie in zip(cols, movies[:8]):
        with col:
            poster = IMAGE_BASE + movie["poster_path"] if movie["poster_path"] else ""
            st.image(poster)

            st.write("⭐", movie["vote_average"])
            st.write(movie["title"])

            if st.button(f"+ Watchlist {movie['id']}"):
                if movie not in st.session_state.watchlist[st.session_state.user]:
                    st.session_state.watchlist[st.session_state.user].append(movie)
                    st.success("เพิ่มแล้ว!")

# -----------------------------
# 🔥 TOP 10
# -----------------------------
elif menu == "🔥 Top 10":
    st.markdown('<div class="title">Top 10 Movies 2025</div>', unsafe_allow_html=True)

    for i, movie in enumerate(movies[:10], start=1):
        col1, col2 = st.columns([1,3])

        with col1:
            poster = IMAGE_BASE + movie["poster_path"]
            st.image(poster)

        with col2:
            st.write(f"#{i} {movie['title']}")
            st.write("⭐", movie["vote_average"])
            st.write(movie["overview"])

        st.markdown("---")

# -----------------------------
# ❤️ WATCHLIST
# -----------------------------
elif menu == "❤️ My Watchlist":
    st.markdown('<div class="title">My Watchlist</div>', unsafe_allow_html=True)

    user_list = st.session_state.watchlist.get(st.session_state.user, [])

    if not user_list:
        st.info("ยังไม่มีหนังใน Watchlist")
    else:
        for movie in user_list:
            col1, col2 = st.columns([1,3])
            with col1:
                poster = IMAGE_BASE + movie["poster_path"]
                st.image(poster)

            with col2:
                st.write(movie["title"])
                st.write("⭐", movie["vote_average"])

                if st.button(f"ลบ {movie['id']}"):
                    st.session_state.watchlist[st.session_state.user].remove(movie)
                    st.rerun()
