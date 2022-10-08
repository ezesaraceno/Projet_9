import logging
import streamlit as st

import azure.functions as func
import pandas as pd
import pickle
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from scipy import sparse




st.write("""
# My Content

An interactive Web app to help people read more by recommending books that they will love.

""")
clicks = pd.read_csv('./clicks_df.csv')

#function that would clean the data
@st.cache

def get_ratings_from_clicks(clicks):
    count_user_article_clicks = (
        clicks.reset_index()
        .groupby(["user_id", "click_article_id"])
        .agg(
            COUNT_user_article_clicks=("index", "count"),
        )
    )

    count_user_clicks = (
        clicks.reset_index()
        .groupby(["user_id"])
        .agg(
            COUNT_user_clicks=("index", "count"),
        )
    )

    ratings = count_user_article_clicks.join(count_user_clicks, on="user_id")
    ratings["rating"] = (
        ratings["COUNT_user_article_clicks"] / ratings["COUNT_user_clicks"]
    )

    ratings = (
        ratings["rating"]
        .reset_index()
        .rename({"click_article_id": "article_id"}, axis=1)
    )

    return ratings


ratings = get_ratings_from_clicks(clicks)

enc = OrdinalEncoder(dtype="int")
ratings_enc = pd.DataFrame(
    enc.fit_transform(ratings[["user_id", "article_id"]]),
    columns=["user_idx", "article_idx"],
)
ratings_enc["rating"] = ratings["rating"]

ratings_sparse = sparse.csr_matrix(
    (
        ratings_enc["rating"].values,
        (ratings_enc["user_idx"].values, ratings_enc["article_idx"].values),
    ),
    shape=(
        ratings_enc["user_idx"].max() + 1,
        ratings_enc["article_idx"].max() + 1,
    ),
)

def get_predictions(user_id, n=10):
    user_articles = set(clicks[clicks["user_id"]==user_id]["click_article_id"].to_list())
    scores = model.recommend(user_id, ratings_sparse[user_id])
    return scores
    

clicks = pd.read_csv('./clicks_df.csv')
left_articles = set(clicks['click_article_id'].to_list())
path = 'C://Users//ezequ//proyectos//openclassrooms//Projet_9//streamlit_azure//model_implicit.pkl'
model = pickle.load(open(path, 'rb'))

selected_user = st.selectbox( "Type or select a user from the dropdown",('1', '2', '3','4', '5', '11183'))
# selected_user = st.selectbox( "Type or select a user from the dropdown", users)#options=list(users.keys()))
# users = clicks["user_id"]
# selected_user = st.selectbox( "Type or select a user from the dropdown", ("1", "2"))#options=list(users.keys()))
st.write('You selected User_ID #:', int(selected_user))

user_id = int(selected_user)

if st.button("Get Recommendation"):
    with st.spinner("Analyzing the library …"):
        ratings = get_ratings_from_clicks(clicks)
        ratings_sparse = ratings_sparse
        prediction = get_predictions(user_id)
        df = pd.DataFrame(prediction)
        df = df.T
        df.columns = ['article_id', 'rating']
        df