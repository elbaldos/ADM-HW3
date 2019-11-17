#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import numpy as np
import io
import os
import plotly.graph_objects as go
import string
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import json
ps = PorterStemmer()
import math
from collections import defaultdict
from collections import Counter
import heapq


# In[2]:


def cleanQ(query):
    query = query.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(query)
    stemmer=[ps.stem(i) for i in tokens]
    filtered_Q = [w for w in stemmer if not w in stopwords.words('english')]
    return filtered_Q


# # 2.1.2) Execute the query

# In[24]:


def SearchEngine1():
    movieDatabase = pd.read_csv(r"C:\Users\HP\Desktop\ADM HW3\searchenginedata1.csv", header=0)
    query = input()
    query=cleanQ(query)
    vocab=json.loads(open("vocabulary.json").read())
    inverted_index = json.loads(open("inverted_index.json").read())
    the_title = []
    the_intro = []
    the_url = []
#     query = [preProcess(word) for word in query]
#     query = [ps.stem(word[0]) for word in query]
    movies = range(50)
    movies = set(movies)
    flag = 0
    for word in query:
        if word in vocab.keys():
            term_id = vocab[word]
            #print(term_id)
            movies = movies.intersection(inverted_index[str(term_id)])
            #print(movies)
        else:
            flag = 1
            return("Not Found")
            break
    if flag == 0:
        for index in movies:
            the_title.append(movieDatabase.Title[index])
            the_intro.append(movieDatabase.Intro[index])
            the_url.append(movieDatabase["URL"][index])
            
        fig = go.Figure(data=[go.Table(header=dict(values=['Title', 'Intro', 'URL']),
                 cells=dict(values=[the_title, the_intro, the_url]))
                     ])
        fig.update_layout(width=2000, height=1000)
        fig.show()


# In[ ]:





# In[139]:


def SearchEngine2():
    query = input()
    query=cleanQ(query)
    the_similarity=[]
    the_title = []
    the_intro = []
    the_url = []
    movies = range(50)
    movies = set(movies)
    # ==================================================================================
    # I_M_P_O_R_T_I_N_G__A_L_L__T_H_E__N_E_C_E_S_S_A_R_Y__S_T_R_U_C_T_U_R_E_S__W_E__N_E_E_D
    # We need the words and their corresponding index for converting the query into the index
    vocab=json.loads(open("vocabulary.json").read())
    # We need the list of documents that have a specific word on it 
    inverted_index = json.loads(open("inverted_index.json").read())
    # We need the tf_idf of the doc i in respect to the term j
    _2nd_inverted_index=json.loads(open("inverted_index_2.json").read())
    # We need as output the title, into and url from the movieDatabase that we've created                               
    movieDatabase = pd.read_csv(r"C:\Users\HP\Desktop\ADM HW3\searchenginedata1.csv", header=0)
    IDF = json.loads(open("idf.json").read())
    #============================
    def TF(doc_words):
        bow = 0
        for k, v in doc_words.items():
            bow = bow + v
        tf_word = {}
        for word, count in doc_words.items():
            tf_word[word] = count / float(bow)
        return tf_word
    # ========================================================
    # C_R_E_A_T_E__T_H_E__V_E_C_T_O_R__F_O_R__T_H_E__Q_U_E_R_Y
    # We are replacing the string with its corresponding integer
    for word in query:
        if word in vocab.keys():
            query[query.index(word)]=(vocab[word])
        else:
            print("word Not found")
    query_vec = {}
    # We are creating a vector that eack component corresponds to the tf_idf for a specific term of the query     
    for word_ in query:
        query_vec[word_]=  TF(Counter(query))[word_]*IDF[str(word_)]
    ##=============================== 
    # C_R_E_A_T_E__T_H_E__V_E_C_T_O_R__F_O_R__E_A_C_H__D_O_C_U_M_E_N_T
    # We are checking which movies have all the terms of the query and we keep only them 
    for word in query: 
        movies = movies.intersection(inverted_index[str(word)]) 
    movieDatabase = movieDatabase.drop(index=movieDatabase.index.difference(movies))
    doc_vec = {}
    for movie in movies:
        vec = []
        for word_ in query:
            index = _2nd_inverted_index[str(word_)]
            for i in range(len(index)):
                if index[i][0] == movie:
                    vec.append(index[i][1])
        doc_vec[movie] = vec
    def dot(vector_1, vector_2):
        sum = 0
        for i in range(len(vector_1)):
            sum = sum + vector_1[i]*vector_2[i]
        return(sum)
    def norm(vector):
        if len(vector) > 1:
            add = 0
            for i in range(len(vector)):
                add = add + vector[i]**2
            return add**(1/2)
        else:
            return(vector)
    similarity = {}
    for movie in movies:
        similarity[movie] = dot(list(query_vec.values()),doc_vec[movie])/norm(list(query_vec.values()))
    the_col = []
    for i in range(len(movieDatabase)):
        for k, v in similarity.items():
            if movieDatabase.index[i] == k:
                the_col.append(similarity[k])
    movieDatabase["Similarity"] = the_col
    truth = []
    for movie_d in movies:
        if movieDatabase["Similarity"][movie_d] in heapq.nlargest(5,movieDatabase["Similarity"]):
            truth.append(movie_d)
    movieDatabase1 = movieDatabase.drop(index=movieDatabase.index.difference(truth))
    return(movieDatabase1)
    for index in truth:
            the_title.append(movieDatabase1.Title[index])
            the_intro.append(movieDatabase1.Intro[index])
            the_url.append(movieDatabase1["URL"][index])
            the_similarity.append(movieDatabase1["Similarity"][index])
    fig = go.Figure(data=[go.Table(header=dict(values=['Title', 'Intro', 'URL', 'Similarity']),
                 cells=dict(values=[the_title, the_intro, the_url, the_similarity]))
                     ])
    fig.update_layout(width=2000, height=1000)
    fig.show()
    

    


# In[77]:


def SearchEngine2(data = pd.read_csv(r"C:\Users\HP\Desktop\ADM HW3\searchenginedata1.csv", header=0)):
    query = input()
    if query == "":
        return("Get Out")
    query=cleanQ(query)
    the_similarity=[]
    the_title = []
    the_intro = []
    the_url = []
    movies = list(data.index)
    movies = set(movies)
    # ==================================================================================
    # I_M_P_O_R_T_I_N_G__A_L_L__T_H_E__N_E_C_E_S_S_A_R_Y__S_T_R_U_C_T_U_R_E_S__W_E__N_E_E_D
    # We need the words and their corresponding index for converting the query into the index
    vocab=json.loads(open("vocabulary.json").read())
    # We need the list of documents that have a specific word on it 
    inverted_index = json.loads(open("inverted_index.json").read())
    # We need the tf_idf of the doc i in respect to the term j
    _2nd_inverted_index=json.loads(open("inverted_index_2.json").read())
    # We need as output the title, into and url from the movieDatabase that we've created                               
    #movieDatabase = pd.read_csv(r"C:\Users\HP\Desktop\ADM HW3\searchenginedata1.csv", header=0)
    IDF = json.loads(open("idf.json").read())
    #data = pd.read_csv(r"C:\Users\HP\Desktop\ADM HW3\searchenginedata1.csv", header=0)
    #============================
    def TF(doc_words):
        bow = 0
        for k, v in doc_words.items():
            bow = bow + v
        tf_word = {}
        for word, count in doc_words.items():
            tf_word[word] = count / float(bow)
        return tf_word
    # ========================================================
    # C_R_E_A_T_E__T_H_E__V_E_C_T_O_R__F_O_R__T_H_E__Q_U_E_R_Y
    # We are replacing the string with its corresponding integer
    for word in query:
        if word in vocab.keys():
            query[query.index(word)]=(vocab[word])
        else:
            print("word Not found")
    query_vec = {}
    # We are creating a vector that eack component corresponds to the tf_idf for a specific term of the query     
    for word_ in query:
        query_vec[word_]=  TF(Counter(query))[word_]*IDF[str(word_)]
    ##=============================== 
    # C_R_E_A_T_E__T_H_E__V_E_C_T_O_R__F_O_R__E_A_C_H__D_O_C_U_M_E_N_T
    # We are checking which movies have all the terms of the query and we keep only them 
    for word in query: 
        movies = movies.intersection(inverted_index[str(word)])
    data = data.drop(index=data.index.difference(movies))
    doc_vec = {}
    for movie in movies:
        vec = []
        for word_ in query:
            index = _2nd_inverted_index[str(word_)]
            for i in range(len(index)):
                if index[i][0] == movie:
                    vec.append(index[i][1])
        doc_vec[movie] = vec
    def dot(vector_1, vector_2):
        sum = 0
        for i in range(len(vector_1)):
            sum = sum + vector_1[i]*vector_2[i]
        return(sum)
    def norm(vector):
        if len(vector) > 1:
            add = 0
            for i in range(len(vector)):
                add = add + vector[i]**2
            return add**(1/2)
        else:
            return(vector)
    similarity = {}
    for movie in movies:
        if isinstance(norm(list(query_vec.values())), float):
            similarity[movie] = dot(list(query_vec.values()),doc_vec[movie])/norm(list(query_vec.values()))
        else:
            similarity[movie] = dot(list(query_vec.values()),doc_vec[movie])/norm(list(query_vec.values()))[0]

    the_col = []
    for i in range(len(data)):
        for k, v in similarity.items():
            if data.index[i] == k:
                the_col.append(similarity[k])
    data["Similarity"] = the_col
    truth = []
    for movie_d in movies:
        if data["Similarity"][movie_d] in heapq.nlargest(5,data["Similarity"]):
            truth.append(movie_d)
    movieDatabase1 = data.drop(index=data.index.difference(truth))
    for index in truth:
            the_title.append(movieDatabase1.Title[index])
            the_intro.append(movieDatabase1.Intro[index])
            the_url.append(movieDatabase1["URL"][index])
            the_similarity.append(movieDatabase1["Similarity"][index])
    fig = go.Figure(data=[go.Table(header=dict(values=['Title', 'Intro', 'URL', 'Similarity']),
                 cells=dict(values=[the_title, the_intro, the_url, the_similarity]))
                     ])
    fig.update_layout(width=2000, height=1000)
    fig.show()
    return(movieDatabase1)
    

    


# In[84]:


def SearchEngine3():
    movie_first = SearchEngine2()
    if isinstance(movie_first, str):
        return("Sorry the search was unsuccessful")
    while True :
        movie_last = movie_first
        movie_first = SearchEngine2(data = movie_last)
        if isinstance(movie_first, str):
            return("Sorry the search was unsuccessful")
            break
    return(movie_last)
    

