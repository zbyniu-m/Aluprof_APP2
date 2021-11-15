# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 22:22:29 2021

@author: USER
"""

import pandas as pd

df = pd.read_csv('data/apple.csv', index_col=0)

# %% omijanie pierwszych wierszy

df_ = pd.read_csv('data/apple.csv', index_col=0, skiprows=10)


df_ = pd.read_csv('data/apple.csv', index_col=0, nrows=100)


# %%

df = pd.read_csv('data/reviews_clean.csv', index_col='id')

# %%

df = pd.read_csv('data/apple.tsv', sep='\t', index_col=0)

# %% xlsx

df = pd.read_excel('data/companies.xlsx', na_values='?', index_col=0)

df_msft = pd.read_excel('data/companies.xlsx', sheet_name='microsoft', index_col=0)

df_google = pd.read_excel('data/companies.xlsx', sheet_name='google', index_col=0)


# %%

df = pd.read_html('data/small.html', header=0, index_col=0)[0]

#%% 

df_ = pd.read_html('https://www.biznesradar.pl/notowania/WIG30#1d_lin_lin')[1]

#%% sas

df=pd.read_sas('data/stocks.sas7bdat')
