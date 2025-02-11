import pickle
import streamlit as st
import pandas as pd
import requests

st.header('Movie Recommendation System')

def fetch_details(movie_name):
    url = "https://www.omdbapi.com/?t={}&apikey=a2edcad8".format(movie_name)
    data = requests.get(url)
    data = data.json()
    details = {
        'poster': data.get('Poster', "https://via.placeholder.com/300"),
        'title': data.get('Title', 'N/A'),
        'year': data.get('Year', 'N/A'),
        'genre': data.get('Genre', 'N/A'),
        'plot': data.get('Plot', 'N/A')
    }
    return details

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_details = []
    for i in movie_list:
        movie_id = i[0]
        movie_name = movies.iloc[movie_id].title
        recommended_movie_details.append(fetch_details(movie_name))

    return recommended_movie_details

# Load movies and similarity data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movie_details = recommend(selected_movie_name)

    col1, col2, col3, col4, col5= st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_details[idx]['title'])
            st.image(recommended_movie_details[idx]['poster'])
            st.caption(f"Year: {recommended_movie_details[idx]['year']}")
            st.caption(f"Genre: {recommended_movie_details[idx]['genre']}")
            st.caption(f"Plot: {recommended_movie_details[idx]['plot']}")

