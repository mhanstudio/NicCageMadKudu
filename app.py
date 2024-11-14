import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Load the data
data = pd.read_csv("imdb-movies-dataset.csv")

# Filter data for movies that feature Nicolas Cage in the cast
cage_data = data[data['Cast'].str.contains("Nicolas Cage", case=False, na=False)]

# Title and introductory text
st.title("Fun Facts about Nicolas Cage's Filmography 🎬")
st.write(f"Nicolas Cage has appeared in {len(cage_data)} movies in this dataset!")

# Display the filtered data as a table
st.subheader("Movies featuring Nicolas Cage")
st.dataframe(cage_data[['Title', 'Year', 'Genre', 'Rating', 'Metascore', 'Votes']])

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
    co_stars = cage_data['Cast'].str.split(',').apply(lambda x: [actor.strip() for actor in x if actor.strip() != "Nicolas Cage"])
    co_star_counter = Counter([actor for sublist in co_stars for actor in sublist])
    top_co_stars = co_star_counter.most_common(10)  # Get the top 10 co-stars
    co_star_names = [actor for actor, _ in top_co_stars]
    co_star_counts = [count for _, count in top_co_stars]
    
    st.write("Here are the top 10 co-stars of Nicolas Cage:")
    st.bar_chart(dict(zip(co_star_names, co_star_counts)))

    # Best and worst-rated Nicolas Cage movies
    st.subheader("Best and Worst-Rated Movies")
    best_movie = cage_data.loc[cage_data['Rating'].idxmax()]
    worst_movie = cage_data.loc[cage_data['Rating'].idxmin()]

    st.write(f"Best-rated movie: {best_movie['Title']} ({best_movie['Rating']})")
    st.write(f"Worst-rated movie: {worst_movie['Title']} ({worst_movie['Rating']})")

    # Average ratings by genre
    st.subheader("Average Ratings by Genre")
    genre_avg_ratings = cage_data.groupby('Genre')['Rating'].mean().sort_values(ascending=False)
    st.bar_chart(genre_avg_ratings)

    # Movie Posters Slideshow
    st.subheader("Movie Posters")
    posters = cage_data['Poster'].dropna().tolist()
    st.write("Here's a slideshow of Nicolas Cage's movie posters!")
    for poster_url in posters:
        st.image(poster_url, width=200)

else:
    st.write("No movies found with Nicolas Cage in this dataset.")
