# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 21:32:18 2019

@author: Afiz
"""

from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
import json

"""
prix de l'électricité:
    https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_03
génération d'hydroélectricité:
    http://api.eia.gov/series/?api_key=d60d4ec7bba3a3b847c218b883a30e52&series_id=ELEC.GEN.HYC-US-98.A
"""
def get_soup(url):
    """
    return the htlm-tree to navigate through
    """

    response = requests.get(url)
    return bs(response.content, "lxml")


def get_data():
    """
    scrap les données de la page et les enregistrent telle quelle au format tsv (tab separated values)
    """
    
    # nom du fichier de donnée que je vais créer
    file_name = "electricity.csv"
            
    #si la clé n'est plus valide, se refaire une clé sur le site de l'EIA
    _url = "http://api.eia.gov/series/?api_key=d60d4ec7bba3a3b847c218b883a30e52&series_id=ELEC.GEN.HYC-US-98.A"
    
    soup = get_soup(_url)    
    content = soup.find(name="p").contents
    data = json.loads(content[0])['series'][0]['data']
    df = pd.DataFrame(data, columns=['datetime', 'electricity_generated'])
    df.to_csv(file_name)
    return df
    