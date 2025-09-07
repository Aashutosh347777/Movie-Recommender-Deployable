import streamlit as st
import pickle 
import pandas as pd
import requests
from dotenv import load_dotenv
import os

films_dict = pickle.load(open('films_dict.pkl','rb'))
films = pd.DataFrame(films_dict)
st.title('Movie Recomendation System')

similarity = pickle.load(open('similarity.pkl','rb'))

def poster_path(id):
    load_dotenv()
    api_key = os.getenv('api_key')
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(id,api_key))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movies):
    mov_index = films[films['title'] == movies].index[0]
    similarity_row = similarity[mov_index]
    sorted_score = sorted(list(enumerate(similarity_row)),reverse = True, key = lambda x:x[1])[1:6]

    recommendations = []
    posters = []

    for score in sorted_score:
        movie_id = films.iloc[score[0]].id  
        recommendations.append(films.iloc[score[0]].title)
        posters.append(poster_path(movie_id))

    return recommendations,posters

selected_movie = st.selectbox(
    'Movies',
    films['title'].values
)

if st.button('Recommend'):
    recommended_movies,images = recommend(selected_movie)
    # for i in recommended_movies:
    #     st.write(i)
    cols = st.columns(5)
    for col, film, image in zip(cols, recommended_movies, images):
        with col:
            st.text(film)
            st.image(image)