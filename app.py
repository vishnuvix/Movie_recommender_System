import streamlit as lt
import pickle
import pandas as pd
import requests


def fetch_image(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


cs = pickle.load(open('cs.pkl', 'rb'))
movies_list = pickle.load(open('movies_name.pkl', 'rb'))
df_ = pd.read_pickle('movies.pkl')


def recommend(movie):
    movie_index = df_[df_['title'] == movie].index[0]
    distance = cs[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = df_.iloc[i[0]].id
        recommended_movies_poster.append(fetch_image(movie_id))
        recommended_movies.append(df_.iloc[i[0]].title)
    return recommended_movies, recommended_movies_poster

lt.title('Movie Recommender System')
option = lt.selectbox('Movies', df_['title'].values)

if lt.button('Recommend'):
    recommended_movies,recommended_movie_posters = recommend(option)
    col1, col2, col3, col4, col5 = lt.columns(5)
    with col1:
        lt.text(recommended_movies[0])
        lt.image(recommended_movie_posters[0])
    with col2:
        lt.text(recommended_movies[1])
        lt.image(recommended_movie_posters[1])

    with col3:
        lt.text(recommended_movies[2])
        lt.image(recommended_movie_posters[2])
    with col4:
        lt.text(recommended_movies[3])
        lt.image(recommended_movie_posters[3])
    with col5:
        lt.text(recommended_movies[4])
        lt.image(recommended_movie_posters[4])



