import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="Movie Popularity Analysis", layout="wide")

# -----------------------
# Netflix Theme
# -----------------------
st.markdown("""
    <style>
    body {
        background-color: #141414;
        color: white;
    }
    .metric-box {
        background-color: #1f1f1f;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Popularity Analysis Dashboard")

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data():
    return pd.read_csv("rotten_tomatoes_movies (1).csv")

df = load_data()

# -----------------------
# ตรวจหาคอลัมน์สำคัญ
# -----------------------
numeric_cols = df.select_dtypes(include="number").columns.tolist()
rating_cols = [c for c in df.columns if "score" in c.lower() or "rating" in c.lower()]
title_col = next((c for c in df.columns if "title" in c.lower()), df.columns[0])
genre_col = next((c for c in df.columns if "genre" in c.lower()), None)

rating_col = rating_cols[0] if rating_cols else numeric_cols[0]

# -----------------------
# KPI Section
# -----------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎬 Total Movies", len(df))

with col2:
    st.metric("⭐ Average Rating", round(df[rating_col].mean(), 2))

with col3:
    st.metric("🏆 Highest Rating", df[rating_col].max())

st.divider()

# -----------------------
# Top 10 Popular Movies
# -----------------------
st.subheader("🔥 Top 10 Highest Rated Movies")

top10 = df.sort_values(by=rating_col, ascending=False).head(10)

st.dataframe(top10[[title_col, rating_col]])

# -----------------------
# Histogram Rating Distribution
# -----------------------
st.subheader("📊 Rating Distribution")

fig, ax = plt.subplots()
ax.hist(df[rating_col].dropna(), bins=20)
ax.set_xlabel("Rating")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# -----------------------
# Genre Analysis
# -----------------------
if genre_col:
    st.subheader("🎭 Genre Analysis")

    genre_count = (
        df[genre_col]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
    )

    fig2, ax2 = plt.subplots()
    genre_count.plot(kind="bar", ax=ax2)
    ax2.set_ylabel("Number of Movies")
    st.pyplot(fig2)
