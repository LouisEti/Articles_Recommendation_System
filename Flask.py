# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 12:25:06 2022

@author: Louis ETIENNE
"""
from flask import Flask, request, send_file, Response, jsonify
import requests
import json
import pandas as pd
import numpy as np 
import os
import pickle
import glob
import datetime
import warnings
import scipy.sparse as sparse
import implicit 
os.environ['MKL_NUM_THREADS'] = '1'

# Flask app creation
app = Flask(__name__)

#Load matricies and implicit model
dir = r"news-portal-user-interactions-by-globocom/"
data_csv = os.path.join(dir, "articles_metadata.csv")
click_sample_csv = os.path.join(dir, "clicks_sample.csv")
articles_embedding_file = os.path.join(dir, "articles_embeddings.pickle")

df_train = pd.read_csv("Implicit_files/df_train.csv")
df_test_read_article = pd.read_csv("Implicit_files/df_test_read_article.csv")
sparse_matrix = sparse.load_npz('Implicit_files/sparse_matrix.npz')
model_als = implicit.cpu.als.AlternatingLeastSquares.load("Implicit_files/model_als.npz")

# =============================================================================
# =============================================================================
# Funtions


def encoded_article_id(original_article_id):
    dict_encoded = dict(enumerate(df_train["article_id"].astype("category").cat.categories))
    list_dict = list(dict_encoded.values())
    index = list_dict.index(original_article_id)

    return index

def decoded_article_id(encoded_article_id):
    dict_encoded = dict(enumerate(df_train["article_id"].astype("category").cat.categories))
    decoded_id = dict_encoded.get(encoded_article_id)

    return decoded_id

def encoded_user_id(original_user_id):
    dict_encoded = dict(enumerate(df_train["user_id"].astype("category").cat.categories))
    list_dict = list(dict_encoded.values())
    index = list_dict.index(original_user_id)

    return index

def decoded_user_id(encoded_user_id):
    dict_encoded = dict(enumerate(df_train["user_id"].astype("category").cat.categories))
    decoded_id = dict_encoded.get(encoded_user_id)

    return decoded_id


def recommend_articles(encoded_user_id):
    """ recommend 5 article ids for a user """
    if encoded_user_id > df_train["encoded_user_id"].max():
        #Cold-start = if user never read an article
        #Chose the 5 most read articles by unique user but not the 5 most read articles 
        articles_id = df_train.groupby("encoded_article_id")["encoded_user_id"].nunique().sort_values(ascending=False).index.tolist()[:5]
        recommend_df = pd.DataFrame({"encoded_article_id_recommended": articles_id})

    else:
        articles_id, score = model_als.recommend(encoded_user_id, sparse_matrix[encoded_user_id], 5)
        recommend_df = pd.DataFrame({"encoded_article_id_recommended": list(articles_id), "score": list(score)})

    decoded_article_id_recommended = []
    for id in articles_id:
        decoded_article_id_recommended.append(decoded_article_id(id))
    
    recommend_df["article_id_recommended"] = decoded_article_id_recommended

    return recommend_df["encoded_article_id_recommended"].tolist()


def true_recommended_als(encoded_user_id_list):
    """ Return encoded articles ids that are recommended for a user and read by him (in df_test)"""
    if type(encoded_user_id_list) != list:
        encoded_user_id_list = [encoded_user_id_list]

    list_recommended = []
    for user_id in encoded_user_id_list:
        # array_recommended_article_id, score = model_als.recommend(user_id, sparse_user_article[user_id],5)
        array_recommended_article_id, score = model_als.recommend(user_id, sparse_matrix[user_id],5)
        list_recommended_article_id = list(array_recommended_article_id) #list of encoded_article_id that are recommended 

        #list of decoded_article_id that are in df_test for encoded_user_id
        list_encoded_article_df_test = df_test_read_article[df_test_read_article["user_id"]==decoded_user_id(user_id)]["encoded_article_id"].tolist()

        #print encoded articles ids that are recommended and in df_test for read articles
        if set(list_recommended_article_id).intersection(list_encoded_article_df_test):
            print({"encoded_user_id": user_id, "encoded_article_id": set(list_recommended_article_id).intersection(list_encoded_article_df_test)})
            list_recommended.append({"encoded_user_id": user_id, "encoded_article_id": set(list_recommended_article_id).intersection(list_encoded_article_df_test)})
        
    return list_recommended, len(list_recommended)


# =============================================================================
# =============================================================================

@app.route('/recommendation', methods=['POST', 'GET'])
def recommendation():  
    
    req = request.form
    user_id = req.get('user_id')
    user_id = int(user_id)
    recommendation = recommend_articles(user_id) #type == list  
    recommendation_list = json.dumps(recommendation) #type == str because a list isn't JSON 
    
    return recommendation_list


# app.run()









