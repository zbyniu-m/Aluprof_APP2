# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 21:41:09 2021

@author: Zbynio
"""

import pandas as pd
import numpy as np

# Przykład 1

s = pd.Series(4)

# Przykład 2

s_def = pd.Series(data=[21,14,54], 
                  index=['adam','tomek','pawel'],
                  name='age')

# Przykład 3

A = np.random.randn(10)
s= pd.Series(A)

# %% Przykład 4

stock = {'Aple':'USA', 'CD-Projekt':'Poland','Amazon':'USA'}
series = pd.Series(stock, name='Country')

# Przykład 5

stock_price = {'Apple': 196, 'CD-Projekt': 215, 'Amazon': 1877}
stock_price_series = pd.Series(stock_price, name='price')

stock_price_array = stock_price_series.values

apple_price = stock_price_series['Apple']

'Apple' in stock_price_series

# %%Przykład 5 

np.random.seed(0)

A = np.random.randn(20)
s = pd.Series(A)

s[0]
s[1]
s[5:10]

# %% podstawowe operacje

np.random.seed(0)

A = np.random.randint(0, 10, 10)

series = pd.Series(A, name='los')

series.dtype
series.iloc[-1]
series.index
series.name
series.shape

array_A = series.values


# %%

N = np.random.randn(10)
M = np.random.randn(10)

series_N = pd.Series(N)
series_M = pd.Series(M)

# %%

series_N.abs()
series_N.add(series_M) # dodawanie
series_N.subtract(series_M)  # odejmowanie
series_N.divide(series_M) # dzielenie
series.drop_duplicates() # usuwanie duplikatów
series[4] = np.nan # wstawiono 4 element jako pusty
series.dropna() # usuwanie pustych pól

series.idxmax() # indeks z maksymalną wartoscią

series.idxmin()

series.count() # zliczanie wartosci

series_N.cumsum() # suma skumulowana

series_N.cummin() # podstawia najmniejsza wartoscia napotkana

series_N.cummax() 

series.value_counts() # listuje wystąpienei elementy

series.sum() # suma
series.std() # odchylenie standardowe
series.describe() # opis statystyczny serii danych


# %% histogram

hist_data = pd.Series(np.random.randn(10000))

hist_data.hist(bins=80, color='red')

# %%
top_3 = series_N.nlargest(3)

bottom_4 = series_N.nsmallest(4)

q_1 = series_N.quantile(0.25)

series_N.round(3)

# %%

shift_1 = series.shift(1)
shist_2_replace_0 = series.shift(2).fillna(0)

# %%

sort_series = series.sort_values()
sort_series = series.sort_values(ascending=False)


#%% agregacja danych

minimum = series.aggregate(min)
maximum = series.aggregate(max)

suma = series.aggregate(sum)

mean = series.aggregate(np.mean)
std = series.aggregate(np.std)

stats = series.aggregate(['min','max','sum','mean'])


#%% apply()

np.random.seed(0)

# sigma = 10, mean = 5
s = pd.Series(10* np.random.randn(20) + 5)

s.apply(abs)
s.apply(float.is_integer)
s.apply(int)

s.apply(lambda x: 100 * x)
s.apply(lambda y: abs(y))

s_norm = s.apply(lambda x: (x - np.mean(s)) / np.std(s))

sigmoid = s_norm.apply(lambda x: 1 / (1 + np.exp(x)))


def more_coplex(x):
    import math
    return math.sqrt(np.exp(x))

s.apply(more_coplex)