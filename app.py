import streamlit as st
import pickle
import pandas as pd
import requests


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_title):
    api_key = '70a57f7e5c6aa61ad52bfe8c3093747a' 
    response = requests.get(
        f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    )
    data = response.json()
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))
    
    return recommended_movies, recommended_posters

st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Choose a movie to get recommendations:',
    movies['title'].values
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)

    st.subheader("Top 5 Similar Movies")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])


def fetch_poster_and_rating(movie_title):
    api_key = '70a57f7e5c6aa61ad52bfe8c3093747a'
    response = requests.get(
        f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    )
    data = response.json()
    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        rating = data['results'][0].get('vote_average', 'N/A')
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            poster_url = "https://via.placeholder.com/500x750?text=No+Image"
        return poster_url, rating
    return "https://via.placeholder.com/500x750?text=No+Image", "N/A"


 # Show Rating

poster_url, rating = fetch_poster_and_rating(selected_movie_name)
st.image(poster_url, caption=selected_movie_name, use_column_width=False , width=200)

if rating != "N/A":
    st.markdown(f"### ⭐ TMDb Rating: {rating}/10")
else:
    st.markdown("Rating: Not Available")

# Redirect to streaming platforms
st.markdown("### 🔗 Where to Watch")

netflix_search_url = f"https://www.netflix.com/search?q={selected_movie_name}"
hotstar_search_url = f"https://www.hotstar.com/in/search?q={selected_movie_name}"
justwatch_url = f"https://www.justwatch.com/in/search?q={selected_movie_name}"

col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.link_button("🎥 Search on Netflix", netflix_search_url, type="primary")
with col2:
    st.link_button("🌟 Search on Hotstar", hotstar_search_url, type="secondary")
with col3:
    st.link_button("🔍 Search on JustWatch", justwatch_url)
