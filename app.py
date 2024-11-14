import streamlit as st
import pandas as pd

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

    # Ratings distribution
    st.subheader("Ratings Distribution")
    st.hist_chart(cage_data['Rating'].dropna())

else:
    st.write("No movies found with Nicolas Cage in this dataset.")

