# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 22:36:37 2021

@author: USER
"""

import numpy as np
import pandas as pd

# %%
df = pd.DataFrame(np.random.randn(20,5), 
                  columns=list('abcde'), 
                  index=list('abcdefghijklmnoprstu'))


# %%  funkcja loc
col_a = df.loc[:,'a']
col_b = df.loc[:,'b']

col_a_b = df.loc[:,['a','b']]

col_b_c_d = df.loc[:,'b':'d']

row_a = df.loc['a',:] # postać series
row_a = df.loc[['a'], :] # postać dataframe

row_a_c = df.loc[['a','c'],:]

row_a_col_a = df.loc['a','a'] # scalar

row_a_d_col_b_d = df.loc['a':'d', 'b':'d']

# %% wycinanie dat

df = pd.DataFrame(np.random.randn(31,5),
                  columns=list('abcde'),
                  index=pd.date_range(start='2019-01-01', periods=31))

# %% wycinanie dat

idx = df.index

day = df.loc['2019-01-02']
week = df.loc['2019-01-01':'2019-01-07']

after_15 = df.loc['2019-01-15':]

before_15 = df.loc[:'2019-01-15']

# %% funkcja iloc
# iloc[row_indexer, column_indexer]

col_1 = df.iloc[:,0]

col_a_b = df.iloc[:,:2]
col_a_b = df.iloc[:,[0,1]]

col_last = df.iloc[:,-1]

col_by_2 = df.iloc[:,::2]

# %% by row

row_1 = df.iloc[0,:] # jako series
 
row_1 = df.iloc[[0],:] # jako dataframe


# %% korpka

col_a = df.a

mask = df.a > 0
out=df[mask]

mask =(df.a > 0) & (df.c >0)
out_2 = df[mask]

mask = (df.a > 0) | (df.b < 0)
out_3 = df[mask]

# %% where


s = pd.Series(np.random.randn(20))

df = pd.DataFrame(np.random.randn(31,2),
                  columns=list('ab'),
                  index=pd.date_range('20190101',periods=31))

out =s[s >0]
out = s.where(s>0)

out = df[df > 0 ]

out = df.where(df > 0)

out =df.where(df > 0, 0) # tam gdzie nie jestdf > 0 wstaw 0

out = df.where(df > 0, 0).where(df < 1, 1)

# %%  Query

df = pd.DataFrame(np.random.rand(10,5),
                  columns=list('abcde'))

df.query('(a < b)')

df.query('(a<b) & (b<c)')

df = df.round(1)

df.query('c == [0.5,0.4,0.3]')
df.query('c!=0.5')

df.query('[0.5,0.7] in c')

# %% index

idx = pd.Index(['8638','0643','0953','3246'])

df = pd.DataFrame(np.random.randn(4,5),
                  index=idx,
                  columns=list('abcde'))


