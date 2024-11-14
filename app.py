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
columns = st.columns(5)  # Corrected indentation here
for i, poster_url in enumerate(posters):
    column_index = i % 5
    columns[column_index].image(poster_url, width=200)

# Display filtered data
st.subheader("Movies featuring Nicolas Cage")
st.dataframe(cage_data[['Title', 'Year', 'Genre', 'Rating', 'Metascore', 'Votes']])

# Best and Worst Rated Films
best_rated = cage_data.loc[cage_data['Rating'].idxmax()]
worst_rated = cage_data.loc[cage_data['Rating'].idxmin()]

st.subheader("Best Rated Film 🎥")
st.write(f"{best_rated['Title']} ({best_rated['Year']}) with a rating of {best_rated['Rating']}")

st.subheader("Worst Rated Film 😞")
st.write(f"{worst_rated['Title']} ({worst_rated['Year']}) with a rating of {worst_rated['Rating']}")

# Average Rating
if not cage_data.empty:
    avg_rating = cage_data['Rating'].mean()
    st.subheader("Average IMDb Rating")
    st.write(f"The average IMDb rating for Nicolas Cage's movies is {avg_rating:.2f}")

    # Total Votes
    cage_data['Votes'] = cage_data['Votes'].replace(",", "", regex=True)
    cage_data['Votes'] = pd.to_numeric(cage_data['Votes'], errors='coerce')
    total_votes = cage_data['Votes'].sum()
    st.subheader("Total IMDb Votes")
    st.write(f"Total votes for Nicolas Cage's movies: {total_votes}")

# Show movie posters as a grid (you can replace these URLs with actual ones)
st.markdown(
    """
    
