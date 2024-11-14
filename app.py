# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title for the app
st.title("Fun Facts about Nicolas Cage's Filmography 🎬")

# Load the CSV data
data = pd.read_csv("https://raw.githubusercontent.com/mhanstudio/NicCageMadKudu/refs/heads/main/imdb-movies-dataset.csv")

st.write(data.columns)

# Display the dataset (optional for user exploration)
if st.checkbox("Show raw data"):
    st.write(data)

# Display the total number of movies
st.subheader("Total Movies 🎥")
st.write(f"Nicolas Cage has appeared in {len(cage_data)} movies!")

# Yearly Movie Count
st.subheader("Movies Per Year")
movies_per_year = cage_data['year'].value_counts().sort_index()
plt.figure(figsize=(10, 5))
plt.plot(movies_per_year.index, movies_per_year.values, marker='o')
plt.xlabel("Year")
plt.ylabel("Number of Movies")
plt.title("Nicolas Cage Movies Per Year")
st.pyplot(plt)

# Average IMDb Rating
st.subheader("Average IMDb Rating ⭐")
avg_rating = cage_data['imdb_rating'].mean()
st.write(f"Average IMDb rating for Nicolas Cage's movies is {avg_rating:.2f}")

# Highest-Rated Movie
st.subheader("Highest-Rated Movie 🌟")
highest_rated_movie = cage_data.loc[cage_data['imdb_rating'].idxmax()]
st.write(f"{highest_rated_movie['title']} ({highest_rated_movie['year']}) with an IMDb rating of {highest_rated_movie['imdb_rating']}")

# Genre Distribution
st.subheader("Genres Nicolas Cage Has Explored")
genres = cage_data['genre'].value_counts()
st.bar_chart(genres)

# Show a subset of the data related to Nicolas Cage's filmography
st.write("Nicolas Cage's Filmography 🎬")
st.write(cage_data)  # Display the filtered data

# Example Visualization: Count of Movies per Year
st.subheader("Number of Nicolas Cage Movies per Year")
movies_per_year = cage_data['year'].value_counts().sort_index()
st.bar_chart(movies_per_year)

st.write("Hope you enjoyed these insights into Nicolas Cage's movie career!")
