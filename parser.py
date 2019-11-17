
#!/usr/bin/env python
# coding: utf-8

# # 1.3 Parse downloaded pages
# 
# #### In the following lines of code we will extract all the valuable and needed information from the saved html files.  We need to extract the title, intro, plot of the movie as well as some ifobox information like director, producer, writter, stars starring in the film, music, release date, running time, country, language and budget.
# #### In the following file you could find the parsing of the movies in movie2.html list. To parse the other files you can change the path directory.

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
from lxml import html
ps = PorterStemmer()


for i in range(10000):
    #reading all the articles
    movie = BeautifulSoup (open(r"C:\Users\HP\Desktop\ADM HW3\movie2\artical_%d.html" %i, encoding="utf8"), features="html")
    # =======================================================================================
    # We have created a function so as to make the information more clear and remove the unicode codes that exist
    def beau(word):
        return(re.sub('[{1}[0-9]*]{1}', '',  word.strip('\n').replace('\xa0', ' ')).split('\n'))
    #=================================================================
    #finding the title of the movie
    for t in movie.select('title'):
        title =(t.text).split(" - ")[0]
    title = "".join(beau(title))
    # ================================================================
    #finding the intro of the movie
    intro = []
    flagi = 0
    # we go through the different layers of html and we search for the specific 
    # paragraph that corresponds to the intro
    for div in movie.findAll("div",{"class":"mw-parser-output"}):
        for p in div.children:
            if p.name == "p":
                intro.append(p.text)
            if p.name == "h2":
                break
    # since we didnt find an intro from the previous code, we will assign the value NaN to it 
    if intro == []:
        intro = float("NaN")
        flagi = 1
    # if the search for the intro was successful we will apply the function to erase any imperfection
    if flagi == 0:
        intro = "".join(beau("".join(intro)))
    # =================================================================
    #finding the plot of the movie
    par = []
    itsin = 0
    flagpp=0
    # we go through the different layers of html and we search for the specific 
    # paragraph that corresponds to the plot(sometimes denoted as plot summary, Plot Summary, Story, Summary etc)
    for section in movie.find_all('h2'):
        for t in section.find_all("span",{'id':'Plot'}):
            itsin = 1
            continue
        for t in section.find_all("span",{'id':'Plot_summary'}): 
            itsin = 1
            continue
        for t in section.find_all("span",{'id':'Plot_Summary'}): 
            itsin = 1
            continue
        for t in section.find_all("span",{'id':'Story'}): 
            itsin = 1
            continue
        for t in section.find_all("span",{'id':'Summary'}): 
            itsin = 1
            continue
        for t in section.find_all("span",{'id':'Premise'}): 
            itsin = 1
            continue
        for t in section.find_all("span",{'id':'Synopsis'}): 
            itsin = 1
            continue
        for t in section.find_all("span",{'id':'Storyline'}): 
            itsin = 1
            continue
        for t in section.find_all("span",{'id':'Storylines'}): 
            itsin = 1
            continue
        # if we find the tag that has attribute "Plot" we follow that and it will lead us to the
        # paragraphs containing the plot
        if itsin == 1:
            for p in section.find_next_siblings():
                if p.name == 'h2':
                    flagpp=1
                    break
                if p.name == "p":
                    par.append(p.text)
                if p.name == "ol":
                    for l in p.find_all("li"):
                        par.append(l.text)
            if flagpp == 1:
                break
    # if we dont find the plot in the previouw way , we try with the h3 way as follows
    if flagpp == 0 and par == []:
        for section in movie.find_all('h3'):
            for t in section.find_all("span",{'id':'Plot'}):
                itsin = 1
                continue
            for p in section.find_next_siblings():
                    if p.name == 'h2':
                        flagpp=1
                        break
                    if p.name == "p":
                        par.append(p.text)
                    if p.name == "ol":
                        for l in p.find_all("li"):
                            par.append(l.text)
            if flagpp == 1:
                break
    # since we didnt find an plot from the previous code, we will assign the value NaN to it 
    if par == []:
        par = float("NaN")
    else:
        par = "".join(beau("".join(par)))
    #===================================================================
    # I_N_F_O_B_O_X
    d = defaultdict(list)
    for div in movie.findAll("div",{"class":"mw-body"}):
        for div1 in div.findAll('div',{"class":"mw-body-content"}):
            for div2 in div1.findAll('div',{"class":"mw-content-ltr"}):
                for table in div2.findAll('table',{"class":"infobox vevent"}):
                    for tr in table.findAll("tr"):
                        for th1 in tr.findAll("th"):
                            for td1 in tr.findAll("td"):
                                for j in range(len(td1.contents)):
                                    attr = []
    # we are creating a dictionary. the keys are the column that correctonds to 
    # Directed by, Produced by etc and the values are the corresponding answers like director, producer etc
                                    try:
                                        attr.append(td1.contents[j].text)
                                        d[th1.text].append(attr)
    # because sometimes the text nodes contain links we use try and except. we use the except part
    # in case we cannot access the information with the try code
                                    except AttributeError:
                                        attr.append(td1.contents[j])
                                        d[th1.text].append(attr)

    # =============================================================================
    # Get only the information that we need
    final_info=[]
    keys = ["Directed by", "Produced by", "Written by", 
       "Starring", "Music by", "Release date", "Running time", 
       "Country", "Language", "Budget"]
    for ele in keys:
        info = ""
        if ele in d.keys():
            if len(ele)>0:
                for i_ in range(0,len(d[ele]),2):
                    info = info  + " " + "".join(beau(d[ele][i_][0]))
            else:
                info = float("NaN")
        final_info.append(info.strip())
    # ============================================================================
    # Correct the unicode issues
    final_info[3] = " ".join(re.findall('[A-Z][^A-Z]*', final_info[3])) 
    # ===========================================================================
    # In the written by place on the infobox there are the information about the original 
    # screenplay and screenplay.. We just summed up all the names
    if "Original screenplay" or "Screenplay" in final_info[2]:
        final_info[2] = final_info[2].replace("Original screenplay" and "Screenplay", "")
    # =====================================================================================
    # All the empty elements are taking the value NaN
    for k in range(len(final_info)):
        if final_info[k] == "" or final_info[k] == ['N/A'] :
            final_info[k] = float("NaN")
    # T_S_V
    data=['Title', 'Intro', 'Plot', 'Directed by','Produced by','Written by','Starring','Music by',
          'Release date','Running time','Country','Language','Budget']      
    with open(r"C:\Users\HP\Desktop\ADM HW3\tsvs\T_S_V_M_2_%d.tsv" %i, 'wt', encoding = 'utf8') as f:
        tsv_file = csv.writer(f, delimiter='\t')
        tsv_file.writerow(data)
        tsv_file.writerow([title, intro, par, final_info[0], final_info[1], final_info[2], final_info[3], final_info[4],final_info[5], final_info[6], final_info[7], final_info[8], final_info[9]])

