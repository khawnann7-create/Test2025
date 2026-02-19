import streamlit as st

st.set_page_config(page_title="Mini Netflix", layout="wide")

# ------------------ Movie Data ------------------
movies = [
    "Interstellar","Inception","The Dark Knight","Titanic",
    "Avengers: Endgame","The Matrix","Joker","Parasite",
    "Top Gun: Maverick","Oppenheimer",
    "ฉลาดเกมส์โกง","พี่มาก..พระโขนง","แฟนฉัน",
    "ร่างทรง","ชัตเตอร์ กดติดวิญญาณ",
    "John Wick","The Conjuring","Dune","Barbie","Frozen"
]

# ------------------ Session ------------------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ------------------ Sidebar ------------------
st.sidebar.title("👤 User")

if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"

if st.sidebar.button("❤️ My Watchlist"):
    st.session_state.page = "Watchlist"

if st.sidebar.button("🗑 Clear Watchlist"):
    st.session_state.watchlist = []

# ------------------ Functions ------------------
def toggle_movie(movie):
    if movie in st.session_state.watchlist:
        st.session_state.watchlist.remove(movie)
    else:
        st.session_state.watchlist.append(movie)

def show_movies(movie_list):
    cols = st.columns(5)  # 5 เรื่องต่อแถว

    for i, movie in enumerate(movie_list):
        with cols[i % 5]:
            st.markdown("### 🎬")
            st.write(movie)

            if movie in st.session_state.watchlist:
                if st.button("Remove", key=f"remove_{movie}_{i}"):
                    toggle_movie(movie)
            else:
                if st.button("Add ❤️", key=f"add_{movie}_{i}"):
                    toggle_movie(movie)

# ------------------ Page ------------------
st.title("🎬 Mini Netflix")

if st.session_state.page == "Home":
    st.subheader("🔥 Popular Movies")
    show_movies(movies)

elif st.session_state.page == "Watchlist":
    st.subheader("❤️ My Watchlist")

    if len(st.session_state.watchlist) == 0:
        st.info("ยังไม่มีหนังใน Watchlist")
    else:
        show_movies(st.session_state.watchlist)
