# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 23:07:50 2021

@author: USER
"""

import numpy as np
import pandas as pd

s = pd.Series(['Apple','     Microsoft',np.nan,'    Google  ','Amazon'], name='stock')

# %%

s = s.str.strip()

# %%

s = s.str.upper()
s = s.str.lower()

s.str.len()


# %%

df = pd.DataFrame(np.random.randn(10,2), columns=['             ID User   ','   Price     '])

# %%
df.columns = df.columns.str.strip()

# %%

df.columns = df.columns.str.replace(' ','_')

# %%

s = pd.Series(['#sport#good#time', '#workout#free#time', '#summer#holiday#hot'],name='hashtag')

s = s.str.split('#')


hash_1=s.str.get(1)
hash_2=s.str.get(2)
hash_3=s.str.get(3)

df_concat_by_row = pd.concat([hash_1, hash_2, hash_3], ignore_index=True)

# jeden string łączący elementy df:
string = df_concat_by_row.str.cat(sep=' ')

df_concat_by_col = pd.concat([hash_1, hash_2, hash_3], ignore_index=True, axis=1)

split_2=s.str.split('#', expand=True)
split_2 = split_2.drop(0, axis=1)

# %%

string = 'worout summer good free holiday time time hot'

split = string.split(' ')

s= pd.Series(split)

# wyraż○enia regularne [0-9] szukamy w tekscie cyfr od 0-9
s.str.contains(r'[0-9]')
# wyraż○enia regularne [a-c] szukamy w tekscie liter od a-c
s.str.contains(r'[a-z]')

# mozna to wykorzystać do wycinanai danych
s.str.contains(r'[rg]')
s[s.str.contains(r'[rg]')]
