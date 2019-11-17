#!/usr/bin/env python
# coding: utf-8

# # Imports
# 

# In[1]:


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
#nltk.download('stopwords')
#nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import json
ps = PorterStemmer()
import math

import index_utils


# #### We will now start working on creating the inverted index.
# #### First since we want to have as an output the url of the movies we will parse the html files again and get the urls

#movies1 = BeautifulSoup (open(r"C:\Users\HP\Documents\GitHub\ADM\2019\Homework_3\data\movies1.html"), features="html")
movies2 = BeautifulSoup (open(r"C:\Users\HP\Documents\GitHub\ADM\2019\Homework_3\data\movies2.html"), features="html")
#movies3 = BeautifulSoup (open(r"C:\Users\HP\Documents\GitHub\ADM\2019\Homework_3\data\movies3.html"), features="html")
movies_links = []
#for url in movies1.find_all("a"):
#    movies_links.append(url.get("href"))
for url in movies2.find_all("a"):
    movies_links.append(url.get("href"))
#for url in movies3.find_all("a"):
#    movies_links.append(url.get("href"))
movies_links[0:3]


# #### We create a function cleanQ so we can do the cleaning and preperation of our data 

####-------function------------------- 
#def cleanQ(query):
# ----------------------------------


# #### Make a dataframe out of our tsv files. This way it will be much easier to compute the components for the inverted index

movieDatabase = pd.read_csv(r"C:\Users\HP\Desktop\ADM HW3\tsvs\T_S_V_M_2_0.tsv", sep='\t', header=0)
#for i in range(1,10000):
#    movieDatabase = movieDatabase.append(pd.read_csv(r"C:\Users\HP\Desktop\ADM HW3\tsvs\T_S_V_M_1_%d.tsv"  %i, sep='\t'), ignore_index=True)
for i in range(1, 50):
    movieDatabase = movieDatabase.append(pd.read_csv(r"C:\Users\HP\Desktop\ADM HW3\tsvs\T_S_V_M_2_%d.tsv"  %i, sep='\t'), ignore_index=True)
#for i in range(10000):
 #   movieDatabase = movieDatabase.append(pd.read_csv(r"C:\Users\HP\Desktop\ADM HW3\tsvs\T_S_V_M_3_%d.tsv"  %i, sep='\t'), ignore_index=True)
movieDatabase["URL"] = movies_links[:50]
movieDatabase.head(3)


# #### Here we will try to clean the data. Usually the movies that dont have a plot and all the information on the infobox
# #### ( if they have an infobox) are movies - links that correspond to disambiguation sites, sites where there are multiple
# #### results with this name. So to improve our engine and the efficiency we delete these entries since its impossible to import them manually

# NULL Checks

truth = []
for i in range(len(movieDatabase)):
    al = (movieDatabase.Plot[i] != movieDatabase.Plot[i] and 
          movieDatabase["Directed by"][i] != movieDatabase["Directed by"][i] and
         movieDatabase["Produced by"][i] != movieDatabase["Produced by"][i] and
         movieDatabase["Written by"][i] != movieDatabase["Written by"][i] and
         movieDatabase["Starring"][i] != movieDatabase["Starring"][i])
    truth.append(not(al))
movieDatabase = movieDatabase[truth]


# #### Knowing that we might have deleted some rows from the dataframe we will assign new indexes to make locating the documents much more easier 

movieDatabase.reset_index(inplace = True)
movieDatabase.drop(columns = ["index"], inplace = True)


# #### Now we will focus on preprocessing all the columns


tmp_intro = []
tmp_title = []
tmp_plot = []
tmp_director = []
tmp_producer = []
tmp_writer = []
tmp_starring = []
tmp_music = []
tmp_date = []
tmp_country = []
tmp_language = []
tmp_time = []
for i in range(len(movieDatabase)):
    if movieDatabase["Intro"][i] == movieDatabase["Intro"][i]:
            tmp_intro.append(index_utils.cleanQ(movieDatabase["Intro"][i]))
    else:
        tmp_intro.append("")
    if movieDatabase["Plot"][i] == movieDatabase["Plot"][i]:
            tmp_plot.append(index_utils.cleanQ(movieDatabase["Plot"][i]))
    else:
        tmp_plot.append("")
    if movieDatabase["Title"][i] == movieDatabase["Title"][i]:
        tmp_title.append(index_utils.cleanQ(movieDatabase["Title"][i]))
    else:
        tmp_title.append("")
    if movieDatabase["Directed by"][i] == movieDatabase["Directed by"][i]:
        tmp_director.append(index_utils.cleanQ(movieDatabase["Directed by"][i]))
    else:
        tmp_director.append("")
    if movieDatabase["Produced by"][i] == movieDatabase["Produced by"][i]:
        tmp_producer.append(index_utils.cleanQ(movieDatabase["Produced by"][i]))
    else:
        tmp_producer.append("")
    if movieDatabase["Written by"][i] == movieDatabase["Written by"][i]:
        tmp_writer.append(index_utils.cleanQ(movieDatabase["Written by"][i]))
    else:
        tmp_writer.append("")
    if movieDatabase["Starring"][i] == movieDatabase["Starring"][i]:
        tmp_starring.append(index_utils.cleanQ(movieDatabase["Starring"][i]))
    else:
        tmp_starring.append("")
    if movieDatabase["Music by"][i] == movieDatabase["Music by"][i]:
        tmp_music.append(index_utils.cleanQ(movieDatabase["Music by"][i]))
    else:
        tmp_music.append("")
    if movieDatabase["Release date"][i] == movieDatabase["Release date"][i]:
        tmp_date.append(index_utils.cleanQ(str(movieDatabase["Release date"][i])))
    else:
        tmp_date.append("")
    if movieDatabase["Country"][i] == movieDatabase["Country"][i]:
        tmp_country.append(index_utils.cleanQ(movieDatabase["Country"][i]))
    else:
        tmp_country.append("")
    if movieDatabase["Language"][i] == movieDatabase["Language"][i]:
        tmp_language.append(index_utils.cleanQ(movieDatabase["Language"][i]))
    else:
        tmp_language.append("")


# #### We are going to find all the words in the documents... Merge them together... And for each row sum them up and make the vocabulary


words=[]  # We are going to use this for creating the vocabulary.
clean_all = [] # This will be a new column with all the preprocessed words of the movie
for i in range(len(movieDatabase)):
    c_all = []
    for wordPl in tmp_plot[i]:
        words.append(wordPl)
        c_all.append(wordPl)
    for wordI in tmp_intro[i]:
        words.append(wordI)
        c_all.append(wordI)
    for wordT in tmp_title[i]:
        words.append(wordT)
        c_all.append(wordT)
    for wordD in tmp_director[i]:
        words.append(wordD)
        c_all.append(wordD)
    for wordPr in tmp_producer[i]:
        words.append(wordPr)
        c_all.append(wordPr)
    for wordW in tmp_writer[i]:
        words.append(wordW)
        c_all.append(wordW)
    for wordM in tmp_music[i]:
        words.append(wordM)
        c_all.append(wordM)
    for wordC in tmp_country[i]:
        words.append(wordC)
        c_all.append(wordC)
    for wordL in tmp_language[i]:
        words.append(wordL)
        c_all.append(wordL)
    clean_all.append(c_all)
movieDatabase["Clean All"] = pd.Series(clean_all)
movieDatabase.head(3)


# #### Create a new Dataframe and save it for future use
# #### We will use searchenginedata1.csv for every search enging

new = movieDatabase[['Title', 'Intro', 'URL']].copy()
new.to_csv("searchenginedata1.csv", index=False, )


# #### Now we create the vocabulary. In the vocalulary there are all the words, and they are accompagnied by an unique index

words=set(words)
words = list(words)
vocab={}
for i in range(len(words)):
    vocab.update({words[i] : i })
with open("vocabulary.json", "w", encoding = "utf8") as v:
    v.write(json.dumps(vocab))


# #### We are replacing the words in the column Clean All with the correponding index that it has on the vocabulary we've created

for i in range(len(movieDatabase)):
    for j in range(len(movieDatabase["Clean All"][i])):
        if movieDatabase["Clean All"][i][j] in vocab.keys():
            movieDatabase["Clean All"][i][j] = vocab[movieDatabase["Clean All"][i][j]]


# #### We are going to change the new col and replace it with a counter dictionary, where every key is a word and the values are the number of times the word apears on the document 


from collections import Counter
movieDatabase["Clean All"] = movieDatabase["Clean All"].apply(lambda x : Counter(x))

TF = []
for i in range(len(movieDatabase["Clean All"])):
    TF.append(computeTF(movieDatabase["Clean All"][i]))
movieDatabase["TF"] = TF

####-------function------------------- 
#def computeTF(doc_words)
# ----------------------------------



# # 2.1.1) Create your index!
# 
# #### We create a dictionary inverted_index. This dictionary has keys the term ids and as corresponding values the list of documents where the term id exists
# ### We save this dictionrary into a JSON file for future use

inverted_index = defaultdict(list)
for i in range(len(movieDatabase)):
    for keys, values in movieDatabase["Clean All"][i].items():
        inverted_index[keys].append(i)
with open("inverted_index.json", "w", encoding = "utf8") as i_d:
    i_d.write(json.dumps(inverted_index))


# # 2.2.1) Inverted Index
# 
# #### We are creating a function to compute the tf_idf of a specific documents and a specific term
# ### We save this dictionrary into a JSON file for future use


idf = {}
for k, v in vocab.items():
    idf[v] = math.log(len(movieDatabase["Clean All"])/len(inverted_index[v]), 10)
with open("idf.json", "w", encoding = "utf8") as i_d_f:
    i_d_f.write(json.dumps(idf))

# We are computing the norm of the tf_idfs for all the documents and terms that exist on those
# movieDatabase["Clean All"] has all the words that exists in the document with the corresponding frequencies
# we store this information in a new column
    
the_norm = []
for i in range(len(movieDatabase)):
    suma = 0
    for word in movieDatabase["Clean All"][i].keys():
        suma = suma + (movieDatabase["TF"][i][word]*idf[word])**2
    the_norm.append(suma**(1/2))
movieDatabase["Norm"] = the_norm


# We are creating idf for all the terms in all the documents and we save it for future use
# We will need it for calculating the tf_idf for the query

idf = {}
for k, v in vocab.items():
    idf[v] = math.log(len(movieDatabase["Clean All"])/len(inverted_index[v]))
with open("idf.json", "w", encoding = "utf8") as i_d_f:
    i_d_f.write(json.dumps(idf))


####-------function------------------- 
#def tf_idf(docid, termid):
# ----------------------------------



# #### We create a dictionary inverted_index_2. This dictionary has keys the term ids and as corresponding values the list of tuples.
# #### These tuples contain the documents where the term id exists and the corresponding NORMALIZED tf_idf

inverted_index_2 = defaultdict(list)
for k, v in inverted_index.items():
    for l in v:
        inverted_index_2[k].append((l, index_utils.tf_idf(l,k)/movieDatabase["Norm"][l]))
with open("inverted_index_2.json", "w", encoding = "utf8") as i_d_2:
    i_d_2.write(json.dumps(inverted_index_2))

