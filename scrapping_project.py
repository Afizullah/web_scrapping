# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:24:57 2019

@author: Afiz
"""

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

rq = requests.get("http://waterdata.usgs.gov/nwis/dv?referred_module=sw&site_no=10290300&site_no=10290400&site_no=10292500&site_no=10297000&site_no=12451200&site_no=12452000&site_no=14070620&group_key=NONE&sitefile_output_format=html_table&column_name=gw_count_nu&range_selection=date_range&begin_date=2010-01-01&end_date=2014-01-01&set_arithscale_y=on&format=html_table&date_format=YYYY-MM-DD&rdb_compression=file&submitted_form=scroll_list", headers=headers)
soup = bs(rq, "html_parser")
table = soup.find_all('table')

print(len(table))
table_row = []
for t in table :
    try:
        rows = t.find_all('tr')
        row_list = list()
    
        for tr in rows:
            td = tr.find_all('td')
            row = [i.text.replace("\xa0", "") for i in td]
            row_list.append(row)
            table_row.append(row_list)
    except:
        pass

    print(row_list)