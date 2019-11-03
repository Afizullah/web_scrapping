"""
Created on Sun Oct 27 21:32:18 2019

@author: Afiz
"""

# =============================================================================
# CE SCRIPT EST INUTILE
# ET LES DONNEES SCRAPPE N'ONT PAS ETE UTILISE DANS L'ANALYSE
# VOILA VOILA
# =============================================================================

from bs4 import BeautifulSoup as bs
import requests
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


def get_data_generated():
    """
    choppe la quantité d'éléctricité généré chaque année
    """

    # nom du fichier de donnée que je vais créer
    file_name = "electricity_generated.csv"

    # si la clé n'est plus valide, se refaire une clé sur le site de l'EIA
    _url = "http://api.eia.gov/series/?api_key=d60d4ec7bba3a3b847c218b883a30e52&series_id=ELEC.GEN.HYC-US-98.A"

    soup = get_soup(_url)
    content = soup.find(name="p").contents
    data = json.loads(content[0])['series'][0]['data']
    df = pd.DataFrame(data, columns=['datetime', 'electricity_generated'])
    df.to_csv(file_name)
    return df


def get_value(tr):

    liste = tr.findAll('td')
    return [el.text.strip().replace('\xa0', " ") for el in liste]


# =============================================================================
# Partie Inutile vu que c'est essentiellement des relevés annuelles
# =============================================================================

def get_data_price():
    
    """
    choppe les prix de l'électricité
    annuel de 2011-2016, mensuel de 2017-présent
    """

    _url = "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_03"

    soup = get_soup(_url)
    node = soup.find('table', attrs={"class": 'table'})
    list_of_table = node.findAll('tr')
    res = [get_value(el) for el in list_of_table]

    # chopper les prix par an indice 0 = année, ind -1 = all sector
    # puis par mois pour 2017, 2018, 2019
    t1 = res.index(['Annual Totals'])
    t2 = res.index(['Year 2017'])
    t3 = res.index(['Year 2018'])
    t4 = res.index(['Year 2019'])
    t5 = res.index(['Year to Date'])

    #[Year, Price]
    Annuals = [[el[0], el[-1]] for el in res[t1+1:t2]]
    #[Month, price]
    Year_2017 = [[el[0], el[-1]] for el in res[t2+1:t3]]
    Year_2018 = [[el[0], el[-1]] for el in res[t3+1:t4]]
    Year_2019 = [[el[0], el[-1]] for el in res[t4+1:t5]]

    dict_month = {month[0]: int(
        index)+1 for (index, month) in enumerate(Year_2017)}
    dict_month = {key: "0" + str(value) if value < 10 else str(value)
                  for (key, value) in dict_month.items()}
    return res, [Annuals, Year_2017, Year_2018, Year_2019], dict_month
