# Algorithmic Methods for Data Mining - Homework 3 
# *What movie to watch tonight?* 
## Group 29: *Salwa Afrah*, *Eleftheria Tetoula Tsonga*, *Andrea Baldino*

<p align="left">
<img src="https://d3c1jucybpy4ua.cloudfront.net/data/63462/big_picture/popcorn.jpg?1567006493" height=430 
</p>

**Goal of the homework**: *Build a search engine over a list of movies that have a dedicated page on Wikipedia.*


The repository consists in the following file:
1. __`README.md`__:
    > a Markdown file that explains the content of your repository. 

2. __`collector.py`__:
    > a python file where we are parsing the `html` files given by our instructors and also the code that enables us to crawl wikipedia and extract the information we need.
3. __`parser.py`__:
    > a python file where we are parsing the extracted `html` pages from wikipedia and we save information like title, intro, plot and infobox in `tsv` files.
4. __`index.py`__:
    > a python file where we clean the data, create the inverted index and calculate the `TF`, `IDF` and `NORMALIZED TF_IDF` for all the movies and the terms within.
5. __`index_utils.py`__:
    > a python file that contains the functions we used for creating the indexes and cleaning the data.
6. __`utils.py`__: 
    > a python file that contains functions we need in more than one of the previous files.
7. __`main.py`__:
    > a python file that contains the functions of the search engines.
8. __`exercise_4.py`__:
    > a python file that contains the implementation of the algorithm that solves problem 4.
9. __`main.ipynb`__: 
    > a Jupyter notebook with all the steps and results of the analysis. In the end, you will be able to select the Engine type.
    > When the user executes the file it will be able to choose:
    >    * `search_engine`: a parameter that the user set to choose the search engine to run. According to the request of the homework, we can get 1,2 or 3.

**Enjoy!!!**
