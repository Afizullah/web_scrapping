# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:24:57 2019

@author: Afiz
"""

from bs4 import BeautifulSoup as bs
import requests
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

## page où se trouve les nom et codes des lacs de l'Oregon, Washington et Californie
url1 = "https://waterdata.usgs.gov/nwis/dv?referred_module=sw&state_cd=ca&state_cd=or&state_cd=wa&site_tp_cd=LK&format=station_list&group_key=NONE&range_selection=days&period=365&begin_date=2018-10-20&end_date=2019-10-19&date_format=YYYY-MM-DD&rdb_compression=file&list_of_search_criteria=state_cd%2Csite_tp_cd%2Crealtime_parameter_selection"
## page avec un tsv des données recherché
url2 = "https://waterdata.usgs.gov/nwis/dv?format=rdb&site_no=09427500&referred_module=sw&period=&begin_date=2013-01-01&end_date=2018-01-01"


def get_soup(url):
    
    """
    return the htlm-tree to navigate through
    """
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    #response = requests.get(url, headers=headers)
    response = requests.get(url)
    return bs(response.content, "lxml")


def get_code_name(soup):
    """
    return [site.code, site.name for in rows]
    """
    
    table_row = soup.findAll("table")[1].findAll("tr")
    return [(tr.findAll("td")[1].string, tr.findAll("td")[2].string) for tr in table_row[1:]]

def generate_url(site_code):
    #09427500
    return "".join(("https://waterdata.usgs.gov/nwis/dv?format=rdb&site_no=", site_code,"&referred_module=sw&period=&begin_date=2013-01-01&end_date=2018-01-01"))


def get_data(site_code, site_name):
    file_name = site_name.strip().replace(" ", "_").replace('/', '-').replace(',','') + ".tsv"
    _url = generate_url(site_code)
    text = get_soup(_url).text
    to_be_parsed = text.split('\n')
    table_rows = [entry for entry in to_be_parsed if "#" not in entry]
    test = "\n".join(table_rows)
    file1 = open("data/"+file_name, "w")
    file1.write(test)
    file1.close()
    return True


soup = get_soup(url1)
Liste = get_code_name(soup)
for code, name in Liste[175:]:
    get_data(code, name)


