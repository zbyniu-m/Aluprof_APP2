# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 23:10:53 2021

@author: USER
"""

import pandas as pd
import numpy as np

#%% 
df= pd.DataFrame(data=[12,34,23])

df = pd.DataFrame(data=[[12,24,35],
                        [53,23,74]], 
                  index=['first','second'], 
                  columns=['col1','col2','col3'])


df = pd.DataFrame(data=[[12,24,35],
                        [53,23,74],
                        [16,17,236]], 
                  index=['first','second','third'], 
                  columns=['col1','col2','col3'])
#%%
d = {'one': pd.Series([1,2,3]),
     'two': pd.Series([4,5,6])}

df = pd.DataFrame(d)

#%%

d = {'one': pd.Series(np.random.randn(100)),
     'two': pd.Series(np.random.randn(100)),
     'three': pd.Series(np.random.randn(100))}

df = pd.DataFrame(d)

#%%

df.index
df.columns

list_of_dicts = [{'apple':1,'orange':4},
                 {'apple':3, 'orange':3,'mango':2}]

df = pd.DataFrame(list_of_dicts)

#%%

for col in df.columns:
    print(col)
    
big_letters= [col.upper() for col in df.columns]

df.columns = big_letters 

#%%

df = pd.read_csv('data/aapl_us_d.csv', index_col=0)
df.columns = ['Open','High', 'Low','Close','Volume']

#%%

open_price = df['Open']

open_price = df.iloc[:,0] # : - wszystkie wiersze, 0 - pierwsza kolumna

close_price = df.Close

last_column = df.iloc[:,-1]

two = df[['Open', 'Low']]

three = df.iloc[:, [0,3,2]]

from_open_to_close = df.iloc[:,0:4]

from_open_to_close = df.iloc[:,:-1]

#%%

df.iloc[:5]
df.iloc[10:20]
df.iloc[10:]

df.iloc[:,:3]
df.iloc[:5,:2]

df.iloc[::2] #co drugi wiersz

# %% obliczenia na kolumnach

df['Average'] = (df['Open'] + df['Close']) / 2.

df['Daily_Change'] = df['Close'] / df['Close'].shift(1)-1 # shift przesunął kolumne o jeden wiersz

df = df.assign(avg=(df['Open'] + df['Close']) / 2.)

max_daily_change = df['Daily_Change'].aggregate(max)
min_daily_change = df['Daily_Change'].aggregate(min)

df['Daily_Change'].hist(bins=100)

df['Flag'] = df['Daily_Change'] >= 0

df['Flag'].aggregate(sum)

days_with_positive_return = df['Flag'].aggregate(sum) / df['Flag'].aggregate('count')

# %% Maska logiczna

df_bool = df > 150

df_= df[df_bool]

df_= df[df>150]

df_2019 = df['2019-01-01':]

df_jan_2019 = df['2019-01-01':'2019-01-31']

df_jan_2019.query('Close > 160')

# %% Szereg czasowy

index = pd.date_range('01-01-2019',periods=10000)
df= pd.DataFrame(np.random.randn(10000), index=index)
df_cumsum = df.cumsum()

df_cumsum.plot(kind='line')


# %% operacje arytmetyczne

df_1 = pd.DataFrame(np.random.randn(10,3), columns=list('ABC'))
df_2 = pd.DataFrame(np.random.randn(10,3), columns=list('ABC'))

df_1 + df_2
df_1 - df_2
df_1 * df_2
df_1 / df_2

df_1 ** 2 # potęga

np.exp(df_1)

# %% próbkowanie danych

sample_10 = df.sample(n=10)

sample_10_percent = df.sample(frac=0.1)

# %% usuwanie duplikatów

df = pd.DataFrame(np.random.randint(0,10,100))

df_unique = df.drop_duplicates()

