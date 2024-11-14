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
    body {
        background: linear-gradient(135deg, #BBD3E5, #D6F0CD);
        color: #333;
    }

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
    <div class="title">🎬 A Quick Summary of Nicolas Cage's Filmography 🌟</div>
    """,
    unsafe_allow_html=True,
)

# Display the dataset (optional for user exploration)
if st.checkbox("Show raw data"):
    st.write(data)

# Show data insights
st.write(f"Nicolas Cage has appeared in {len(cage_data)} movies in this dataset!")

# Movie Posters Slideshow
st.subheader("Movie Posters")
st.write(f"Check out some of the posters from his films:")
posters = cage_data['Poster'].dropna().tolist()

# Create a grid of movie posters (5 per row)
columns = st.columns(5)  
for i, poster_url in enumerate(posters):
    column_index = i % 5
    columns[column_index].image(poster_url, width=200)

# Display filtered data
st.subheader("Titles featuring Nicolas Cage")
st.dataframe(cage_data[['Title', 'Year', 'Genre', 'Rating', 'Metascore', 'Votes']])

# What About His Best and Worst Rated Films?
best_rated = cage_data.loc[cage_data['Rating'].idxmax()]
worst_rated = cage_data.loc[cage_data['Rating'].idxmin()]

st.subheader("Best Rated Film 💪")
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

# Average Ratings by Genre
st.subheader("Average Ratings by Genre 🎬")
genre_ratings = cage_data.groupby('Genre')['Rating'].mean()
st.bar_chart(genre_ratings)

# Co-stars
co_stars = cage_data['Cast'].str.split(",").explode().str.strip()

# Filter out Nicolas Cage from co-stars
co_stars = co_stars[co_stars != "Nicolas Cage"]

# Count the most frequent co-stars and get the top 10
co_star_counts = co_stars.value_counts().head(10)

# Display the chart
st.subheader("Most Frequent Co-Stars 🌟")
st.bar_chart(co_star_counts)

# Movie Duration Distribution
st.subheader("How Long Are His Movies?")
plt.figure(figsize=(10, 6))
plt.hist(cage_data['Duration (min)'], bins=15, color='orange', edgecolor='black')
plt.title('Distribution of Movie Durations for Nicolas Cage Movies')
plt.xlabel('Duration (minutes)')
plt.ylabel('Frequency')
st.pyplot(plt)

# Wordcloud of Reviews
reviews = ' '.join(cage_data['Review'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(reviews)
st.subheader("Most Common Words That Appear in Reviews 📝")
st.image(wordcloud.to_array())

# Add footer for extra flair
st.markdown(
    """
    <style>
    footer {
        visibility: hidden;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #FF6347; text-align: center; color: white; padding: 10px;">
    Thanks for reading! Created with ❤️ by Mona
    </div>
    """, 
    unsafe_allow_html=True
)
