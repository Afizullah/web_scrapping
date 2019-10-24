# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import numpy as np
import scipy as sc
import pandas as pd
import matplotlib as plt
from bs4 import BeautifulSoup
from requests import get

url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
response = get(url)
#print(response.text[:500])
html_soup = BeautifulSoup(response.text, 'html.parser')
print(type(html_soup))
movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')

'''
print(type(movie_containers))
print(len(movie_containers))
first_movie = movie_containers[0]
print(first_movie)
#print(first_movie.div)
#print(first_movie.h3)
#print(first_movie.h3.a)
first_name = first_movie.h3.a.text
first_year = first_movie.h3.find('span', class_ = 'lister-item-year text-muted unbold')
first_imdb = float(first_movie.strong.text)
first_mscore = first_movie.find('span', class_ = 'metascore favorable')
first_mscore = int(first_mscore.text)
print(first_mscore)
first_votes = first_movie.find('span', attrs = {'name':'nv'})
print(first_votes)
first_votes = int(first_votes['data-value'])
print(first_votes)
eighth_movie_mscore = movie_containers[7].find('div', class_ = 'ratings-metascore')
type(eighth_movie_mscore)
'''


def ScrapIMDB(movie_containers):
    # Lists to store the scraped data in
    names = []
    years = []
    imdb_ratings = []
    metascores = []
    votes = []
    
    # Extract data from individual movie container
    for container in movie_containers:

        # If the movie has Metascore, then extract:
        if container.find('div', class_ = 'ratings-metascore') is not None:
    
            # The name
            name = container.h3.a.text
            names.append(name)
    
            # The year
            year = container.h3.find('span', class_ = 'lister-item-year').text
            years.append(year)
    
            # The IMDB rating
            imdb = float(container.strong.text)
            imdb_ratings.append(imdb)
    
            # The Metascore
            m_score = container.find('span', class_ = 'metascore').text
            metascores.append(int(m_score))
    
            # The number of votes
            vote = container.find('span', attrs = {'name':'nv'})['data-value']
            votes.append(int(vote))
    print("ok Scrapped "+str(len(names)))
    
ScrapIMDB(movie_containers)