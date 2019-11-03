# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 22:36:24 2019

@author: Afiz
"""

import requests
import pandas as pd
import numpy as np

def download_data():
    
    for i in range(1,7):    
        dl = "https://www.eia.gov/electricity/data/eia861m/archive/xls/f826201"+str(i)+".xls"
        resp = requests.get(dl)
        output = open("price/201"+str(i)+".xls", 'wb')
        output.write(resp.content)
        output.close()
        
    for i in range(7,9):    
        dl = "https://www.eia.gov/electricity/data/eia861m/archive/xls/retail_sales_201"+str(i)+".xlsx"
        resp = requests.get(dl)
        output = open("price/201"+str(i)+".xls", 'wb')
        output.write(resp.content)
        output.close()
        

def format_date(df):
    df = df.copy()
    df['datetime'] = df['YEAR'].apply(str)+'-'+df['MONTH'].apply(lambda x : "0" + str(int(x)) if x < 10 else str(int(x)))
    return df.drop(columns=['YEAR', 'MONTH'])



def format_1(_df):
    #df = pd.read_excel("price/2011.xlsx")
    df = _df.loc[_df.STATE_CODE.isin(['CA', 'OR', 'WA'])]
    df = df[['STATE_CODE' , 'YEAR', 'MONTH', 'TOT_REV (Thousand $)', 'TOT_SALES (MWh)']]
    df = format_date(df).reset_index(drop=True)
    df = df.groupby('datetime', as_index=False).sum()
    df['price']= df["TOT_REV (Thousand $)"] / df["TOT_SALES (MWh)"]
    df = df.drop(columns=["TOT_REV (Thousand $)", "TOT_SALES (MWh)"])
    return df


def format_2(_df):
    df = _df.loc[_df.STATE_CODE.isin(['CA', 'OR', 'WA'])]
    df = df[['STATE_CODE' , 'YEAR', 'MONTH', 'TOTAL REVENUES ($1,000)', 'TOTAL SALES (MWh)']]
    df = format_date(df).reset_index(drop=True)
    df = df.groupby('datetime', as_index=False).sum()
    df['price'] = df['TOTAL REVENUES ($1,000)'] / df['TOTAL SALES (MWh)']
    df = df.drop(columns=['TOTAL REVENUES ($1,000)', "TOTAL SALES (MWh)"])
    return df
    
def format_3(_df):
    df = _df.loc[_df.State.isin(['CA', 'OR', 'WA'])]
    df = df[['State' , 'Year', 'Month', 'Thousands Dollars.4', 'Megawatthours.4']]
    df = df.rename(columns={'Year' : 'YEAR', "Month" : "MONTH"})
    df = format_date(df).reset_index(drop=True)
    df['Megawatthours.4'] = df['Megawatthours.4'].apply(np.float64)
    df['Thousands Dollars.4'] = df['Thousands Dollars.4'].apply(np.float64)
    df = df.groupby('datetime', as_index=False).sum()
    df['price'] = df['Thousands Dollars.4'] / df['Megawatthours.4']
    df = df.drop(columns=['Thousands Dollars.4', 'Megawatthours.4'])
    return df

def create_data():
    dfs = []
    df = pd.read_excel("price/2011.xls")
    df = format_1(df)
    dfs.append(df)
    df = pd.read_excel("price/2012.xls")
    df = format_2(df)
    dfs.append(df)
    for i in range(3,9):
        print(i)
        _df = pd.read_excel("price/201"+str(i)+".xls", header=2)
        _df = format_3(_df)
        dfs.append(_df)
    df = pd.concat(dfs, ignore_index=True)
    return df

resultat = create_data()
resultat.to_csv("price.csv")