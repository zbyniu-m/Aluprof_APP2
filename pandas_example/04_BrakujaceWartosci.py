# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 21:43:35 2021

@author: USER
"""

import pandas as pd
import numpy as np

# %%

df = pd.DataFrame(np.random.randn(10,4),
                  columns=['one','two','three','four'])

# %%

for row in df.values:
    i = np.random.choice([0,1,2,3])
    row[i] = np.nan
    
# %%

for row in df.values:
    switch = np.random.choice([0,1])
    if switch:
        i = np.random.choice([0,1,2,3])
        row[i] = np.nan


# %% isnull()

df.isnull()

df['one'].isnull()

df[df['one'].isnull()]

df[~df['one'].isnull()]

#%% notnull(

df.notnull()

df[df.notnull()]

df['one'].notnull()

df[df['one'].notnull()]

#%%

df['five'] = np.nan

#%% usuwanie

del df['five']

#%% wypełnianie

df = df.fillna(0)

df['one'] = df['one'].fillna(0)

#%%
df = df.fillna(df.mean())

#%%
df= df.fillna(df.mediana())

df['four'] = df['four'].fillna(df['four'].mean)

#%%

df.describe()

df.dropna() # usuwa wiersze z brakami
df.dropna(axis=1) # usuwa kolumny z brakami


