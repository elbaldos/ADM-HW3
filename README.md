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
    > a python file that contains the line of code needed to collect our data from the `html` page (from which we get the urls) and Wikipedia.
0. __`collector_utils.py`__:
    > a python file that stores the function we used in `collector.py`.
2. __`parser.py`__:
    > a python file that contains the line of code needed to parse the entire collection of `html` pages and save those in `tsv` files.
4. __`parser_utils.py`__:
    > a python file that gathers the function we used in `parser.py`.
5. __`index.py`__:
    > a python file that once executed generate the indexes of the Search engines.
6. __`index_utils.py`__:
    > a python file that contains the functions we used for creating indexes.
7. __`utils.py`__: 
    > a python file that gather functions we need in more than one of the previous files like (`collector`, `parser`, etc.)
8. __`main.py`__:
    > a python file that once executed build up the search engine. This file is very important because it is going to be the one we will launch during the exam, indeed we will perform live queries on your search engine. In order to let everything go the best, you have to be sure that the engine will work on pre-computed indeces. Thus, **forget to allow the main file to build the index from scratch**.
    
    > When the user executes the file it will be able to choose:
    >    * `search_engine`: a parameter that the user set to choose the search engine to run. According to the request of the homework, we can get 1,2 or 3.
    >  	* Any other parameters you would like.
9. __`exercise_4.py`__:
    > a python file that contains the implementation of the algorithm that solves problem 4.

10. __`main.ipynb`__: 
    > a Jupyter notebook explaines the strategies we adopted solving the homework and the Bonus point (visualization task). 
        
        Example of Results from the Search Engines
          1. Conjunctive query
          2. Conjunctive query & Ranking score  
          3. Stars query & Magic score
