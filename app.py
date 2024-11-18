import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import altair as alt

# Load the data
data = pd.read_csv("imdb-movies-dataset.csv")

# Filter data for Nicolas Cage movies
cage_data = data[data['Cast'].str.contains("Nicolas Cage", case=False, na=False)]

# Introduction
st.title("Exploring Nicolas Cage's Cinematic Journey 🎬")
st.markdown(
    """
    Nicolas Cage is a name that stands out in Hollywood, known for his diverse roles ranging from blockbuster action films to quirky indie dramas. 
    His career has spanned decades, delivering unforgettable performances across numerous genres. With this app, let's dive into his filmography 
    and uncover some fascinating insights about his movies, ratings, and impact on audiences. Ready to explore? Let's get started!
    """
)

# Display the dataset (optional for user exploration)
if st.checkbox("Show raw data"):
    st.write(data)

# Total Movies
st.subheader("How Prolific is Nicolas Cage?")
st.write(f"According to our dataset, Nicolas Cage has appeared in **{len(cage_data)} movies**.")
st.markdown(
    """
    Cage's prolific nature as an actor is evident. From high-octane action to heartfelt dramas, his versatility knows no bounds. 
    But what genres does he excel in? Let’s explore the distribution of genres in his filmography.
    """
)

st.markdown(
        """
        First - a quick glance at Nicolas Cage's movies shows just how visually striking and diverse his filmography is. 
        Each poster tells its own story, reflecting the unique energy and themes of each film.
        """
    )

# Movie Posters Slideshow
st.subheader("Movie Posters")
st.write(f"Check out some of the posters here:")
posters = cage_data['Poster'].dropna().tolist()

# Create a grid of movie posters (5 per row)
columns = st.columns(5)  
for i, poster_url in enumerate(posters):
    column_index = i % 5
    columns[column_index].image(poster_url, width=200)



# Genre Distribution
st.subheader("Genres of Nicolas Cage's Movies")
genre_counts = cage_data['Genre'].str.get_dummies(sep=', ').sum().sort_values(ascending=False)
st.bar_chart(genre_counts)
st.markdown(
    """
    Nicolas Cage's filmography spans a wide array of genres, with **Action**, **Drama**, and **Thriller** taking the lead. 
    This aligns with his reputation as a versatile actor capable of delivering high-energy performances and emotionally charged roles alike.
    """
)

# Top and Lowest Rated Movies
st.subheader("Cage's Top & Lowest Rated Movies")
if not cage_data.empty:
    top_movie = cage_data.loc[cage_data['Rating'].idxmax()]
    lowest_movie = cage_data.loc[cage_data['Rating'].idxmin()]

    col1, col2 = st.columns(2)

    with col1:
        st.image(top_movie['Poster'], caption=f"Top Rated: {top_movie['Title']} ({top_movie['Rating']})", use_column_width=True)

    with col2:
        st.image(lowest_movie['Poster'], caption=f"Lowest Rated: {lowest_movie['Title']} ({lowest_movie['Rating']})", use_column_width=True)

    st.markdown(
        """
        Cage’s highest-rated movie showcases his talent at its peak, while his lowest-rated work might offer insights into 
        the challenges of maintaining consistent critical acclaim over a long career.
        """
    )

# Average Rating
if not cage_data.empty:
    avg_rating = cage_data['Rating'].mean()
    st.subheader("How Do Audiences Rate Nicolas Cage's Movies?")
    st.write(f"On average, Nicolas Cage's movies hold an IMDb rating of **{avg_rating:.2f}**.")
    st.markdown(
        """
        This shows that while Cage's filmography is vast, his movies maintain consistent audience appeal. 
        Let’s dive deeper to see how these ratings are distributed.
        """
    )

    # Ratings Distribution
    st.subheader("Distribution of IMDb Ratings")
    rating_distribution = (
        alt.Chart(cage_data)
        .mark_bar()
        .encode(
            alt.X("Rating:Q", bin=alt.Bin(maxbins=20), title="IMDb Rating"),
            alt.Y("count():Q", title="Number of Movies"),
            tooltip=["Rating:Q"]
        )
        .properties(title="Histogram of IMDb Ratings", width=600)
    )

    st.altair_chart(rating_distribution, use_container_width=True)
    st.markdown(
        """
        The ratings distribution reveals that most of Cage’s films fall within the **6 to 8 range** on IMDb, indicating a generally favorable 
        reception. However, there are outliers—movies that either didn’t resonate with audiences or became cult classics over time.
        """
    )

# Wordcloud of Reviews
reviews = ' '.join(cage_data['Review'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='#E5F0F9').generate(reviews)
st.subheader("Most Common Words That Appear in Reviews 📝")
st.image(wordcloud.to_array())

    
# Total votes analysis
st.subheader("Total Votes for Nicolas Cage's Movies")
try:
    total_votes = cage_data['Votes'].replace(",", "", regex=True).astype(int).sum()
    st.write(f"Across all movies, Nicolas Cage's films have accumulated a total of **{total_votes:,} votes** on IMDb.")
except Exception as e:
    st.write("An error occurred while processing the votes. Please check the dataset.")

# Conclusion
st.subheader("Wrapping Up Nicolas Cage’s Filmography")
st.markdown(
    """
    Nicolas Cage's career is a testament to the power of versatility and dedication to craft. His ability to take on diverse roles 
    and appeal to a wide audience has solidified his place as a Hollywood icon. From blockbuster hits to underrated gems, 
    his filmography tells a story of bold choices and an unrelenting drive to entertain.
    
    Whether you're a fan of Cage's action-packed adventures or his emotionally nuanced performances, there’s no denying that his legacy 
    in cinema is both fascinating and enduring.
    """
)

# Add footer for extra flair
st.markdown(
    """
    <div class="footer">
        Thanks for reading! Created with ❤️ by Mona
    </div>
    """, 
    unsafe_allow_html=True
)
