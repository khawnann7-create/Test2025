import streamlit as st
import pandas as pd

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="Netflix Movie Ranking", layout="wide")

# -----------------------
# Netflix Theme CSS
# -----------------------
st.markdown("""
    <style>
    body {
        background-color: #141414;
        color: white;
    }
    .movie-card {
        background-color: #1f1f1f;
        padding: 10px;
        border-radius: 10px;
        transition: 0.3s;
        text-align: center;
    }
    .movie-card:hover {
        transform: scale(1.05);
    }
    .title {
        font-size:16px;
        font-weight:bold;
        color:white;
        margin-top:5px;
    }
    .rating {
        color:#E50914;
        font-size:14px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 NETFLIX STYLE MOVIE RANKING")
st.markdown("### 🔥 Top 10 Movies by Highest Rating")

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("rotten_tomatoes_movies (1).csv")
    return df

df = load_data()

# -----------------------
# หา column คะแนน
# -----------------------
rating_columns = [col for col in df.columns if "score" in col.lower() or "rating" in col.lower()]
if rating_columns:
    rating_col = rating_columns[0]
else:
    rating_col = df.select_dtypes(include="number").columns[0]

# หา column ชื่อหนัง
title_col = None
for col in df.columns:
    if "title" in col.lower():
        title_col = col
        break
if title_col is None:
    title_col = df.columns[0]

# หา column poster
poster_col = None
for col in df.columns:
    if "poster" in col.lower() or "image" in col.lower():
        poster_col = col
        break

# -----------------------
# Top 10
# -----------------------
top10 = df.sort_values(by=rating_col, ascending=False).head(10)

# -----------------------
# Display Grid
# -----------------------
cols = st.columns(5)

for i, (_, row) in enumerate(top10.iterrows()):
    with cols[i % 5]:

        # แสดงโปสเตอร์ถ้ามี
        if poster_col and pd.notna(row[poster_col]):
            st.image(row[poster_col], use_container_width=True)
        else:
            st.image("https://via.placeholder.com/300x450?text=No+Image", use_container_width=True)

        st.markdown(f"""
            <div class="movie-card">
                <div class="title">{row[title_col]}</div>
                <div class="rating">⭐ {row[rating_col]}</div>
            </div>
        """, unsafe_allow_html=True)
