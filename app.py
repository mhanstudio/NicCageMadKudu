import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob

# Load data
data = pd.read_csv("imdb-movies-dataset.csv")

# Filter data for Nicolas Cage movies
cage_data = data[data['Cast'].str.contains("Nicolas Cage", case=False, na=False)]

# Styling the title with markdown for a fun look
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 50px;
        color: #FF6347;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        background-color: #FFFAF0;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    <div class="title">🎬 Fun Facts About Nicolas Cage's Filmography 🌟</div>
    """,
    unsafe_allow_html=True,
)

# Show data insights
st.write(f"Nicolas Cage has appeared in {len(cage_data)} movies in this dataset!")

# Movie Posters Slideshow
st.subheader("Movie Posters")
posters = cage_data['Poster'].dropna().tolist()

# Create a grid of movie posters (5 per row)
columns = st.columns(5)  
for i, poster_url in enumerate(poste
