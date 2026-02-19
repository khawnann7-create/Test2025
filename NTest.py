import streamlit as st
import requests
import random

st.set_page_config(page_title="Mini Netflix", layout="wide")

# ---------------------------
# โหลดหนังจาก OMDb ฟรี (ไม่ต้อง API Key)
# ---------------------------
@st.cache_data
def load_movies():
    sample_titles = [
        "Avengers","Batman","Superman","Spider Man","Iron Man",
        "Frozen","Titanic","Inception","Interstellar","Joker",
        "Harry Potter","Lord of the Rings","Fast and Furious",
        "Transformers","Mission Impossible","John Wick",
        "Parasite","Train to Busan","Top Gun","Dune",
        "Barbie","Oppenheimer","Matrix","Gladiator","Whiplash",
        "The Conjuring","Insidious","Annabelle","The Nun",
        "Coco","Up","Toy Story","Aladdin","Mulan",
        "Shutter Island","Fight Club","The Prestige",
        "The Dark Knight","The Godfather"
    ]

    movies = []

    for title in sample_titles:
        url = f"http://www.omdbapi.com/?apikey=thewdb&t={title}"
        try:
            res = requests.get(url, timeout=5)
            data = res.json()
            if data.get("Response") == "True":
                movies.append(data)
        except:
            pass

    # ทำซ้ำให้ได้เยอะขึ้น
    movies = movies * 5  # ได้ประมาณ 200 เรื่อง
    random.shuffle(movies)
    return movies

movies = load_movies()

# ---------------------------
# Session
# ---------------------------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("🎬 Mini Netflix")

if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"

if st.sidebar.button("❤️ My Watchlist"):
    st.session_state.page = "Watchlist"

if st.sidebar.button("🗑 Clear Watchlist"):
    st.session_state.watchlist = []

search = st.sidebar.text_input("🔎 Search")

# ---------------------------
# Functions
# ---------------------------
def toggle_watchlist(movie):
    if movie in st.session_state.watchlist:
        st.session_state.watchlist.remove(movie)
    else:
        st.session_state.watchlist.append(movie)

def show_movies(movie_list):
    cols = st.columns(5)

    for i, movie in enumerate(movie_list):
        with cols[i % 5]:
            poster = movie.get("Poster")
            if poster and poster != "N/A":
                st.image(poster)
            else:
                st.image("https://via.placeholder.com/300x450?text=No+Image")

            st.write(f"**{movie.get('Title')} ({movie.get('Year')})**")

            if movie in st.session_state.watchlist:
                if st.button("Remove ❤️", key=f"r_{movie['imdbID']}_{i}"):
                    toggle_watchlist(movie)
            else:
                if st.button("Add ❤️", key=f"a_{movie['imdbID']}_{i}"):
                    toggle_watchlist(movie)

# ---------------------------
# UI
# ---------------------------
st.title("🔥 Mini Netflix Clone")

if st.session_state.page == "Home":

    filtered = movies
    if search:
        filtered = [
            m for m in movies
            if search.lower() in m.get("Title","").lower()
        ]

    show_movies(filtered)

elif st.session_state.page == "Watchlist":

    st.header("❤️ My Watchlist")

    if not st.session_state.watchlist:
        st.info("ยังไม่มีหนังใน Watchlist")
    else:
        show_movies(st.session_state.watchlist)
