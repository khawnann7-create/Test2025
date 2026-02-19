import streamlit as st
import requests

st.set_page_config(page_title="Mini Netflix", layout="wide")

# -------------------------------
# 🔑 ใส่ API KEY ตรงนี้
# -------------------------------
TMDB_API_KEY = "PUT_YOUR_TMDB_KEY_HERE"

# -------------------------------
# Session
# -------------------------------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

# -------------------------------
# ดึงหนังจาก TMDB
# -------------------------------
@st.cache_data
def get_movies(pages=3):  # เพิ่ม pages เพื่อให้ได้หนังเยอะ
    all_movies = []
    for page in range(1, pages + 1):
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&page={page}"
        res = requests.get(url)
        data = res.json()
        all_movies.extend(data["results"])
    return all_movies

movies = get_movies(pages=5)  # 5 หน้า ≈ 100 เรื่อง

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("🎬 Mini Netflix")

if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"

if st.sidebar.button("❤️ My Watchlist"):
    st.session_state.page = "Watchlist"

if st.sidebar.button("🗑 Clear Watchlist"):
    st.session_state.watchlist = []

# -------------------------------
# Functions
# -------------------------------
def toggle_watchlist(movie):
    if movie in st.session_state.watchlist:
        st.session_state.watchlist.remove(movie)
    else:
        st.session_state.watchlist.append(movie)

def show_movies(movie_list):
    cols = st.columns(5)

    for i, movie in enumerate(movie_list):
        with cols[i % 5]:
            poster_path = movie.get("poster_path")
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                st.image(poster_url)
            else:
                st.write("No Image")

            st.write(f"**{movie['title']}**")

            if movie in st.session_state.watchlist:
                if st.button("Remove ❤️", key=f"remove_{movie['id']}"):
                    toggle_watchlist(movie)
            else:
                if st.button("Add ❤️", key=f"add_{movie['id']}"):
                    toggle_watchlist(movie)

# -------------------------------
# Page
# -------------------------------
st.title("🔥 Mini Netflix")

if st.session_state.page == "Home":
    show_movies(movies)

elif st.session_state.page == "Watchlist":
    st.header("❤️ My Watchlist")

    if len(st.session_state.watchlist) == 0:
        st.info("ยังไม่มีหนังใน Watchlist")
    else:
        show_movies(st.session_state.watchlist)
