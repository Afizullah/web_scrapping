# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:24:57 2019

@author: Afiz
"""

from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
"""

useful url:
    https://waterdata.usgs.gov/nwis/?tab_delimited_format_info
    https://help.waterdata.usgs.gov/output-formats
    https://help.waterdata.usgs.gov/tutorials
    https://help.waterdata.usgs.gov/tutorials/overview
    https://help.waterdata.usgs.gov/tutorials/overview/navigating-usgs-water-data-for-the-nation
    https://help.waterdata.usgs.gov/faq/automated-retrievals#GWLevels
    https://help.waterdata.usgs.gov/tutorials/surface-water-data/how-do-i-access-historical-streamflow-data
    https://waterdata.usgs.gov/nwis/dv?referred_module=sw&state_cd=ca&state_cd=or&state_cd=wa&site_tp_cd=LK&format=station_list&group_key=NONE&range_selection=days&period=365&begin_date=2018-10-20&end_date=2019-10-19&date_format=YYYY-MM-DD&rdb_compression=file&list_of_search_criteria=state_cd%2Csite_tp_cd%2Crealtime_parameter_selection
    https://waterdata.usgs.gov/nwis/dv?cb_00054=on&format=gif_default&site_no=10270700&referred_module=sw&period=&begin_date=2018-10-19&end_date=2019-10-19
    https://waterdata.usgs.gov/nwis/dv?format=rdb&site_no=09427500&referred_module=sw&period=&begin_date=2013-01-01&end_date=2018-01-01

    (old)    
    https://waterdata.usgs.gov/nwis/dv?cb_00054=on&cb_00065=on&format=rdb&site_no=09427500&referred_module=sw&period=&begin_date=2013-01-01&end_date=2018-01-01
    http://waterdata.usgs.gov/nwis/dv?referred_module=sw&site_no=10290300&site_no=10290400&site_no=10292500&site_no=10297000&site_no=12451200&site_no=12452000&site_no=14070620&group_key=NONE&sitefile_output_format=html_table&column_name=gw_count_nu&range_selection=date_range&begin_date=2010-01-01&end_date=2014-01-01&set_arithscale_y=on&format=html_table&date_format=YYYY-MM-DD&rdb_compression=file&submitted_form=scroll_list
"""

# page où se trouve les nom et codes des sources d'eaus de l'Oregon, Washington et Californie
url1 = "https://waterdata.usgs.gov/nwis/dv?referred_module=sw&state_cd=ca&state_cd=or&state_cd=wa&site_tp_cd=LK&format=station_list&group_key=NONE&range_selection=days&period=365&begin_date=2018-10-20&end_date=2019-10-19&date_format=YYYY-MM-DD&rdb_compression=file&list_of_search_criteria=state_cd%2Csite_tp_cd%2Crealtime_parameter_selection"
# page avec un tsv des données recherché pour un lac random entre le 01/01/2011 et le 01/01/2018
# url2 = "https://waterdata.usgs.gov/nwis/dv?format=rdb&site_no=09427500&referred_module=sw&period=&begin_date=2011-01-01&end_date=2018-01-01"


def get_soup(url):
    """
    return the htlm-tree to navigate through
    """

    response = requests.get(url)
    return bs(response.content, "lxml")


def get_code_name(soup):
    """
    renvoit [site.code, site.name for in rows]
    """
    
    table_row = soup.findAll("table")[1].findAll("tr")
    return [(tr.findAll("td")[1].string, tr.findAll("td")[2].string) for tr in table_row[1:]]

def generate_url(site_code):
    """
    renvoit l'url de la page du lac/réservoir à scrapper à partir de son code
    """
    
    return "".join(("https://waterdata.usgs.gov/nwis/dv?format=rdb&site_no=", site_code,"&referred_module=sw&period=&begin_date=2011-01-01&end_date=2018-01-01"))


def get_data(site_code, site_name):
    """
    scrap les données de la page et les enregistrent telle quelle au format tsv (tab separated values)
    """
    
    # nom du fichier de donnée que je vais créer
    file_name = site_name.strip().replace(" ", "_").replace(
            '/', '-').replace(',','_') + ".tsv"
            
    _url = generate_url(site_code)
    
    #on obtient tout le texte de la page
    text = get_soup(_url).text

    #on sépare par ligne
    to_be_parsed = text.split('\n')
    
    #enlève les commentaire
    table_rows = [entry for entry in to_be_parsed if "#" not in entry]
    
    #enlève la description des lignes 
    table_rows.pop(1)
    
    #reforme le résultat
    content = "\n".join(table_rows)
    
    #ouvre un fichier
    file1 = open("water/"+file_name, "w")
    file1.write(content)
    file1.close()
    
    return None

def scrap(url):
    """
    
    """
    soup = get_soup(url)
    # liste de paires [code du lac/réservoir, nom]
    Liste = get_code_name(soup)
    
    # on choppe les données de tous les lacs/réservoirs et on les écrits dans des fichier
    # ça prend environ ~10 min de scrapper les pages de 324 point d'eau qui nous intéressent
    for code, name in Liste:
        get_data(code, name)
        
    for file in os.listdir("water"):
        if (os.stat("water/" + file).st_size < 50_000) or ("LAKE" not in file and "RESERVOIR" not in file):
            print(file)
            os.remove("water/" + file)
            

def format_dataframes():
    """
    Formate toutes les données récoltées pour crée les csv des données des différents lieux
    """
    
    for file in os.listdir("water"):
        
        df = pd.read_csv("water/" + file, sep="\t")
        df = df.drop(columns=['agency_cd', 'site_no'])
        for col in df.columns:
            if df[col][0] == 'A':
                df.drop(columns=col, inplace=True)
                
        #fait une interpolation lineaire pour inférer les données manquantes
        df.interpolate(method="linear", limit_direction="both", inplace=True)
        
        # fait la somme de toutes les colonnes avec des valeurs numériques 
        # pour obtenir le volume d'eau totale des différents points d'eau du lieu
        
        df = pd.concat((df['datetime'], df[df.columns[1:]].sum(axis=1)), axis=1)
        
        #renomme la colonne du volume d'eau avec le nom du lieu
        df.rename(columns={df.columns[1] : file[:-3]}, inplace=True)
        try:
            os.remove("series/" + file[:-3] + "csv")
        except:
            pass
        df.to_csv("series/" + file[:-3] + "csv")

def create_data():
    """
    créer un fichier water.csv qui est le dataframe finale contenant toute nos données, proprement formaté
    """
    
    #lit le premier csv du répertoire des csv
    df = pd.read_csv("series/" + os.listdir("series")[0], index_col=0)
    
    # le fusionne avec les suivants
    for file in os.listdir("water_series")[1:]:
        df_bis = pd.read_csv("water_series/" + file, index_col=0)
        #fusionne les dataframes à partir de la date
        df = df.merge(df_bis, on='datetime', how='outer', copy=False)
        
    # utilise une interpolation linaire pour inférer le niveau d'eau les jours manquants
    df.interpolate(method="linear", limit_direction="both", inplace=True)
    df.sort_values(by='datetime')
    df.to_csv('water_level.csv')
    
    return df

def main(url):
    """
    fonction principale à executer pour faire appel à tout ce qu'il y a au dessus
    """
    scrap(url)
    format_dataframes()
    return create_data()

df = main(url1)