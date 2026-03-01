import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Netflix Movie Dashboard", layout="wide")

# -----------------------------
# NETFLIX STYLE CSS
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #141414;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
.metric-box {
    background-color: #1f1f1f;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Netflix Movie Popularity Dashboard")
st.markdown("### 🔥 วิเคราะห์ภาพยนตร์ยอดนิยม")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("rotten_tomatoes_movies (1).csv")

df = load_data()

# -----------------------------
# AUTO DETECT COLUMNS
# -----------------------------
numeric_cols = df.select_dtypes(include="number").columns.tolist()

rating_cols = [c for c in df.columns if "score" in c.lower() or "rating" in c.lower()]
title_col = next((c for c in df.columns if "title" in c.lower()), df.columns[0])
genre_col = next((c for c in df.columns if "genre" in c.lower()), None)
year_col = next((c for c in df.columns if "year" in c.lower()), None)

rating_col = rating_cols[0] if rating_cols else numeric_cols[0]

# -----------------------------
# KPI SECTION
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("🎬 Total Movies", len(df))
col2.metric("⭐ Average Rating", round(df[rating_col].mean(), 2))
col3.metric("🏆 Highest Rating", df[rating_col].max())

st.divider()

# -----------------------------
# TOP 10 MOVIES
# -----------------------------
st.subheader("🔥 Top 10 Highest Rated Movies")

top10 = df.sort_values(by=rating_col, ascending=False).head(10)

fig_top10 = px.bar(
    top10,
    x=rating_col,
    y=title_col,
    orientation='h',
    color=rating_col,
    color_continuous_scale="Reds"
)

fig_top10.update_layout(
    template="plotly_dark",
    yaxis=dict(autorange="reversed"),
    height=500
)

st.plotly_chart(fig_top10, use_container_width=True)

# -----------------------------
# RATING DISTRIBUTION
# -----------------------------
st.subheader("📊 Rating Distribution")

fig_hist = px.histogram(
    df,
    x=rating_col,
    nbins=20,
    color_discrete_sequence=["#E50914"]
)

fig_hist.update_layout(template="plotly_dark")
st.plotly_chart(fig_hist, use_container_width=True)

# -----------------------------
# GENRE ANALYSIS
# -----------------------------
if genre_col:
    st.subheader("🎭 Top Genres")

    genre_data = (
        df[genre_col]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
        .reset_index()
    )

    genre_data.columns = ["Genre", "Count"]

    fig_genre = px.bar(
        genre_data,
        x="Genre",
        y="Count",
        color="Count",
        color_continuous_scale="Reds"
    )

    fig_genre.update_layout(template="plotly_dark")
    st.plotly_chart(fig_genre, use_container_width=True)

# -----------------------------
# YEAR TREND
# -----------------------------
if year_col:
    st.subheader("📅 Movies Released Per Year")

    year_data = df[year_col].value_counts().sort_index().reset_index()
    year_data.columns = ["Year", "Count"]

    fig_year = px.line(
        year_data,
        x="Year",
        y="Count",
        markers=True
    )

    fig_year.update_layout(template="plotly_dark")
    st.plotly_chart(fig_year, use_container_width=True)
