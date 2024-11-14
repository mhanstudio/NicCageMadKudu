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

# Display filtered data
st.subheader("Movies featuring Nicolas Cage")
st.dataframe(cage_data[['Title', 'Year', 'Genre', 'Rating', 'Metascore', 'Votes']])

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

# Show movie posters as a grid
st.markdown(
    """
    <div style="display: flex; flex-wrap: wrap; justify-content: space-evenly;">
        <img src="https://link-to-poster-1.com" style="width: 200px; height: 300px; margin: 10px;">
        <img src="https://link-to-poster-2.com" style="width: 200px; height: 300px; margin: 10px;">
        <img src="https://link-to-poster-3.com" style="width: 200px; height: 300px; margin: 10px;">
    </div>
    """, 
    unsafe_allow_html=True
)

# Adding more fun insights...
st.subheader("Average Ratings by Genre")
genre_ratings = cage_data.groupby('Genre')['Rating'].mean()
st.bar_chart(genre_ratings)

# Co-stars
co_stars = cage_data['Cast'].str.split(",").explode().str.strip().value_counts().head(10)
st.subheader("Top 10 Co-Stars")
st.bar_chart(co_stars)

# Wordcloud of Reviews
reviews = ' '.join(cage_data['Review'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(reviews)
st.image(wordcloud.to_array())

# Footer for extra flair
st.markdown(
    """
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #FF6347; text-align: center; color: white; padding: 10px;">
    Created with ❤️ by [Your Name]
    </div>
    """, 
    unsafe_allow_html=True
)
