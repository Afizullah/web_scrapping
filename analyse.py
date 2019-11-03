# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 01:39:51 2019

@author: Afiz
"""

import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose


price = pd.read_csv("price.csv", index_col=0)
water = pd.read_csv("water_level.csv", index_col=0)
water = pd.concat([water[water.columns[1:]].sum(
    axis=1), water['datetime']], axis=1)
water = water.rename(columns={0: "level"})

water.datetime = pd.to_datetime(water.datetime)
price.datetime = pd.to_datetime(price.datetime)

df = pd.merge(price, water, on='datetime', how='outer')

df.level = df.level/df.level.max()
df.price = df.price/df.price.max()

df = df.sort_values('datetime')
df = df.reset_index(drop=True)
df.level.interpolate(method='linear', limit_direction='both', inplace=True)
df.price.interpolate(method='linear', limit_direction='both', inplace=True)


df.plot(x='datetime', y=['price', 'level'], figsize=(10, 5))

price = price.set_index('datetime', drop=True)
price_decomp = seasonal_decompose(price, model='additive',freq=12)

water = water.set_index('datetime', drop=True)
water_decomp = seasonal_decompose(water, model='additive',freq=12)

price_decomp.plot()
water_decomp.plot()