import streamlit as st
import pickle
import pandas as pd
import requests
st.title('Movies Recommendation')
# for api

def fetch_poster(movie_id):
    # here The TMDB is not working properly due to which the api refred is not able to fetch image data
    url = "".format(movie_id)
    response=requests.get(url)
    data=response.json()
    poster_path=data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
#recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movies_list= sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        fetched_movie_poster=fetch_poster(movie_id)
        recommended_movies_poster.append(fetched_movie_poster)
    return recommended_movies,recommended_movies_poster
# for movie select we use text box

movies_dict=pickle.load(open("movies_dict.pkl","rb"))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open("similarity.pkl","rb"))

movie_list = movies['title'].values
selected_movie_name=st.selectbox('"Type or select a movie from the dropdown",',(movie_list))

# to show selected movie name
if st.button("Show Recommendation"):
    names,posters=recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])