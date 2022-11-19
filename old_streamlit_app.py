import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import base64
# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#         f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
#         background-size: cover
#     }}
#     </style>
#     """,
#         unsafe_allow_html=True
#     )
#
#
# add_bg_from_local("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/01_Streamlit/st_background.png")


df_film = pd.read_pickle("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/df_films.p")
df_titres = pd.read_pickle("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/df_titres.p")
df = pd.read_pickle("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/df_algo.p")




### ALGO
scaler = MinMaxScaler()
df = scaler.fit_transform(df)
X = df
algo = NearestNeighbors(n_neighbors=6)
algo.fit(X)




