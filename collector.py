#!/usr/bin/env python
# coding: utf-8

# # 1.1. Get the list of movies
# 
# #### We will start by using the html files given to us by the instructor. In these html files (3 html files) are 10.000 links for wikipedia pages regarding movies. At this step we will get the links of these movies, that later will use to crawl Wikipedia.


# Get the movies from the html page
movies1 = BeautifulSoup (open(r"C:\Users\HP\Documents\GitHub\ADM\2019\Homework_3\data\movies1.html"), features="html")
movies2 = BeautifulSoup (open(r"C:\Users\HP\Documents\GitHub\ADM\2019\Homework_3\data\movies2.html"), features="html")
movies3 = BeautifulSoup (open(r"C:\Users\HP\Documents\GitHub\ADM\2019\Homework_3\data\movies3.html"), features="html")
# Initialize the list we are going to use
movies1_links = []
movies2_links = []
movies3_links = []
# Foa all the movies found in the html, we append them to the lists accordingy
for url in movies1.find_all("a"):
    movies1_links.append(url.get("href"))
for url in movies2.find_all("a"):
    movies2_links.append(url.get("href"))
for url in movies3.find_all("a"):
    movies3_links.append(url.get("href"))                                               


# # 1.2. Crawl Wikipedia
# 
# #### Now it's time to crawl the Wikipedia page. With the links we got from the previous step we crawl the page and then we save the html locally as "artical_" and the movie number it refers to. Here is the code we used for movies1 list.

# for the indexes and the elements(links) in  the list movies1_list we extract all the information 
# and save it to "artical_(number of index)"
for index , url in enumerate(movies1_links):
    try:
        page = requests.get(url)
    except :
        print("An error occured.")
        time.sleep(1200)
        continue
        
    soup = BeautifulSoup(page.text,'html.parser')
    file=open("artical_%s.html" % index,"w")
    file.write(str(soup))
    file.close()
    time.sleep(2)

