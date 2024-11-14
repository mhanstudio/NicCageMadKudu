import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from wordcloud import WordCloud
from textblob import TextBlob

# Load the data
data = pd.read_csv("imdb-movies-dataset.csv")

# Filter data for movies that feature Nicolas Cage in the cast
cage_data = data[data['Cast'].str.contains("Nicolas Cage", case=False, na=False)]

# Title and introductory text
st.title("Fun Facts about Nicolas Cage's Filmography 🎬")
st.write(f"Nicolas Cage has appeared in {len(cage_data)} movies in this dataset!")

# Display the filtered data as a table
st.subheader("Movies featuring Nicolas Cage")
st.dataframe(cage_data[['Title', 'Year', 'Genre', 'Rating', 'Metascore', 'Votes', 'Duration (min)', 'Review Count']])

# Additional insights
if not cage_data.empty:
    # Display average rating
    avg_rating = cage_data['Rating'].mean()
    st.subheader("Average IMDb Rating")
    st.write(f"The average IMDb rating for Nicolas Cage's movies is {avg_rating:.2f}")

    # Display total votes
    cage_data['Votes'] = cage_data['Votes'].replace(",", "", regex=True)
    cage_data['Votes'] = pd.to_numeric(cage_data['Votes'], errors='coerce')
    total_votes = cage_data['Votes'].sum()
    st.subheader("Total IMDb Votes")
    st.write(f"Total votes for Nicolas Cage's movies: {total_votes}")

    # Genre distribution
    st.subheader("Genres of Nicolas Cage's Movies")
    genre_counts = cage_data['Genre'].str.get_dummies(sep=', ').sum().sort_values(ascending=False)
    st.bar_chart(genre_counts)

    # Ratings distribution (fixed with matplotlib)
    st.subheader("Ratings Distribution")
    ratings = cage_data['Rating'].dropna()
    plt.figure(figsize=(10, 6))
    plt.hist(ratings, bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of Ratings for Nicolas Cage Movies')
    plt.xlabel('IMDb Rating')
    plt.ylabel('Frequency')
    st.pyplot(plt)

    # Who does Nicolas Cage most commonly co-star with?
    st.subheader("Top Co-Stars")
    cage_data['Cast'] = cage_data['Cast'].fillna("").apply(lambda x: x.split(',') if x else [])
    co_stars = cage_data['Cast'].apply(lambda x: [actor.strip() for actor in x if actor.strip() != "Nicolas Cage"])
    co_star_counter = Counter([actor for sublist in co_stars for actor in sublist])
    top_co_stars = co_star_counter.most_common(10)

    if top_co_stars:
        co_star_names = [actor for actor, _ in top_co_stars]
        co_star_counts = [count for _, count in top_co_stars]
        st.bar_chart(dict(zip(co_star_names, co_star_counts)))
    else:
        st.write("No co-stars found in the dataset.")

    # Movie Duration Distribution
    st.subheader("Movie Duration Distribution")
    plt.figure(figsize=(10, 6))
    plt.hist(cage_data['Duration (min)'], bins=15, color='orange', edgecolor='black')
    plt.title('Distribution of Movie Durations for Nicolas Cage Movies')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Frequency')
    st.pyplot(plt)

    # Word Cloud for Review Titles
    st.subheader("Most Common Review Titles (Word Cloud)")
    review_titles = " ".join(cage_data['Review Title'].dropna().tolist())
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(review_titles)
    st.image(wordcloud.to_array(), caption="Word Cloud of Review Titles")

    # Review Sentiment Analysis (Using TextBlob)
    st.subheader("Sentiment Analysis of Reviews")
    sentiment_scores = cage_data['Review'].dropna().apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    sentiment_avg = sentiment_scores.mean()

    st.write(f"Average sentiment of all reviews: {sentiment_avg:.2f}")
    st.write("Sentiment score ranges from -1 (negative) to +1 (positive). Positive scores indicate favorable reviews, while negative ones suggest critical reviews.")

    # Movie Posters Slideshow
    st.subheader("Movie Posters")
    posters = cage_data['Poster'].dropna().tolist()

    # Create a grid of movie posters (5 per row)
    columns = st.columns(5)
    for i, poster_url in enumerate(posters):
        column_index = i % 5
        columns[column_index].image(poster_url, width=200)

else:
    st.write("No movies found with Nicolas Cage in this dataset.")
