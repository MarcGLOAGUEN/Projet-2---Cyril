import streamlit as st
import pandas as pd
import random
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import streamlit as st
from streamlit_chat import message
import time

st.set_page_config(
    page_title="Cyril by m&m's",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


## importation des tables pour l'algo
df_film = pd.read_pickle("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/df_films.p")
df_titres = pd.read_pickle("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/df_titres.p")
df_algo = pd.read_pickle("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/df_algo.p")
df_algo.drop(df_algo.loc[:,"10":'zombie'],axis=1,inplace=True)

### scaled des données
scaler = MinMaxScaler()
X = scaler.fit_transform(df_algo)

### gestion des poids
p_startYear = 1.5
p_runtimeM = 0.4
p_averageR = 0.5
p_numVote = 0.5
p_actor = 1.6
p_director = 1.5
p_genres = 1.4
p_country = 1.3

X[:,0] *= p_startYear
X[:,1] *= p_runtimeM
X[:,2] *= p_averageR
X[:,3] *= p_numVote
X[:,4:1878] *= p_actor
X[:,1878:2549] *= p_director
X[:,2549:2573] *= p_genres
X[:,2573:] *= p_country

#ajustement personaliser genres
X[:,2551] *= 2 # Animation
X[:,2556] *= 0.5 # Drama
X[:,2553] *= 0.8 # Comedy

#ajustement personaliser director
poids_director = 1.5
X[:,1986] *= poids_director # Nolan
X[:,2404] *= poids_director # Tarantino
X[:,2483] *= poids_director # Spielberg
X[:,2423] *= poids_director # Ridley Scott
X[:,2498] *= poids_director # Tim Burton
X[:,2388] *= poids_director #Peter Jackson

### Initialisation de l'algo
algo = NearestNeighbors(n_neighbors=6)
algo.fit(X)

poster = False

if "bot" not in st.session_state:
    st.session_state["bot"] = ["Si tu n’as pas d’idée de film à regarder, donne-moi un film que tu as aimé récemment. Je te proposerai 5 films similaires que tu pourrais aimer 😉",
                               "Salut, moi c'est Cyril, malgrès mon jeune âge j'ai déjà vu 8274 films 😅."
                               ]
    st.session_state["user"] = []
    st.session_state["poster"] = []
    st.session_state["title"] = []







### HEADER
st.image("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/01_Streamlit/st_header.png", use_column_width = True)



col_chat,col_ligne1, col_poster1, col_poster2,col_poster3,col_poster4,col_poster5,col_ligne2 = st.columns([30,5,10,10,10,10,10,5])

with col_chat :
    film = st.selectbox(" ",options = ([" "]+list(df_titres.Title)))
    if st.button("Envoyer"):
        if film == " ":
            st.session_state.bot.append("...")
            st.session_state.user.append("...")
            st.session_state.bot.append("Tu peux taper un titre approchant en anglais ou français, je compléterai automatiquement 😉 ")
            st.session_state.bot.append("Oups 🫢, il me semble que tu n'as pas choisi de film")
        else :
            tconst_film = df_titres[(df_titres.Title == film)].index.item()
            distance, indices = algo.kneighbors(X[df_film.index == tconst_film])
            film_choose = film[:-7] + " de " + film[-5:-1]
            st.session_state.bot.append(film_choose)
            st.session_state.user.append(film_choose)
            st.session_state.poster.append(df_film.loc[tconst_film, :].Poster)
            st.session_state.poster.append("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/01_Streamlit/st_espace_vide.png")
            st.session_state.title.append(df_film.loc[tconst_film, :].originalTitle)
            st.session_state.title.append("")


            if df_film.loc[tconst_film,"averageRating"] < 6 :
                    list_badanwser = ["Ah vraiment ... tu fais donc partit des gens qui ont aimé ce film...","Vérifie tu as du mal taper 🧐 tu est sûr de ton choix"]
                    st.session_state.bot.append(list_badanwser[random.randrange(len(list_badanwser))])
            else :
                if df_film.loc[[tconst_film],:].genres.str.contains("Horror").item() :
                    st.session_state.bot.append(" Oh ! un film qui fait peur 😨")
                else :
                    list_A = [
                        "Oui ! Très bon choix !",
                        film[:-7] + ", j'ai adoré ce film !",
                        "Oh ! ça fait longtemps que je ne l'ai pas vu",
                        "Et oui !!! 💪🏻  ",
                        "Je l'ai vu hier, très bonne idée 💡"
                        ]
                    try :
                        list_B = [
                            "Très bonne idée, j'aime beaucoup " + df_film.loc[tconst_film, "Actor"].split(",")[random.randrange(len(df_film.loc[tconst_film, "Actor"].split(",")))] + " dans ce film",
                            df_film.loc[tconst_film, "Director"].split(",")[0] + " est un très bon réalisateur",
                            "Bon choix j'aime bien les films de " + df_film.loc[tconst_film, "Director"].split(",")[random.randrange(len(df_film.loc[tconst_film, "Director"].split(",")))],
                            ]
                        list_answer = list_A + list_B

                    except :
                        list_answer = list_A

                    st.session_state.bot.append(list_answer[random.randrange(len(list_answer))])
            poster = True

    if st.session_state["bot"]:
        counter = 0
        for i in range(len(st.session_state["bot"]) - 1,-1, -1):
            if st.session_state["bot"][i] in st.session_state["user"] :
                message(st.session_state["bot"][i], key=str(i), is_user=True)
            else :
                message(st.session_state["bot"][i], key=str(i))
            counter += 1
            if counter >5 :
                break
            else :
                continue



def print_film(numero) :
    st.image("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/01_Streamlit/st_espace_vide.png")
    st.image("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/01_Streamlit/st_espace_vide.png")
    st.image("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/01_Streamlit/st_espace_vide.png")
    st.image(df_film.iloc[list(indices[0])[numero], :].Poster)
    st.image("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/01_Streamlit/st_espace_vide2.png")
    url = "https://www.imdb.com/title/"+df_film.iloc[[list(indices[0])[numero]], :].index.item()
    st.write(f"[{df_film.iloc[list(indices[0])[numero], :].originalTitle}](%s)" % url)
    st.write(str(int(df_film.iloc[list(indices[0])[numero], :].startYear)))
    st.write("⭐",str(df_film.iloc[list(indices[0])[numero], :].averageRating))

with col_ligne1 :
    st.image("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/01_Streamlit/st_ligne_vertical.png")
with col_poster1 :
    if poster :
        with st.spinner('Wait for it...'):
            time.sleep(3)
        print_film(1)
        st.session_state.poster.append(df_film.iloc[list(indices[0])[1], :].Poster)
        st.session_state.title.append(df_film.iloc[list(indices[0])[1], :].originalTitle)

with col_poster2 :
    if poster :
        print_film(2)
        st.session_state.poster.append(df_film.iloc[list(indices[0])[2], :].Poster)
        st.session_state.title.append(df_film.iloc[list(indices[0])[2], :].originalTitle)
with col_poster3 :
    if poster :
        print_film(3)
        st.session_state.poster.append(df_film.iloc[list(indices[0])[3], :].Poster)
        st.session_state.title.append(df_film.iloc[list(indices[0])[3], :].originalTitle)
with col_poster4 :
    if poster :
        print_film(4)
        st.session_state.poster.append(df_film.iloc[list(indices[0])[4], :].Poster)
        st.session_state.title.append(df_film.iloc[list(indices[0])[4], :].originalTitle)
with col_poster5 :
    if poster :
        print_film(5)
        st.session_state.poster.append(df_film.iloc[list(indices[0])[5], :].Poster)
        st.session_state.title.append(df_film.iloc[list(indices[0])[5], :].originalTitle)

with col_ligne2 :
    st.image("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/01_Streamlit/st_ligne_vertical.png")



st.image("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/01_Streamlit/st_espace_vide.png")
st.image("/Users/marc/Mon Drive/02_Wild Code/03_Projets/02_Projet 2/01_Streamlit/st_footer.png")


col_hist1, col_hist2 = st.columns([1,10])
with col_hist2 :
    if st.session_state["poster"]:
        for i in range(len(st.session_state["poster"]) - 14,-1, -7):
            st.image(st.session_state["poster"][i:i+7], caption = st.session_state["title"][i:i+7], width=150)


