# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 23:26:03 2021

@author: USER
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# %%

ts = pd.Series(np.random.randn(1000), 
               index=pd.date_range('2019-01-01', periods=1000))

# %%

ts = ts.cumsum()
ts.plot()

# %%

ts = ts.cummin()
ts.plot()

# %%

ts = ts.cummax()
ts.plot()

# %%


df = pd.DataFrame(np.random.randn(1000,5), 
               index=pd.date_range('2019-01-01', periods=1000),
               columns=list('ABCDE'))

# %%

df = df.cumsum()
df.plot()

# %%

df['B'].plot()

# %%

abs(df.iloc[5]).plot(kind='bar', title='bar chart')

# %% wykres słupkowy

df = pd.DataFrame(np.random.rand(100,4), columns=list('ABCD'))

df = df.cumsum()
bar_data=df.iloc[-1].apply(abs)

bar_data.plot(kind='bar', title='Random generated data', color='green', alpha=0.5)

# %%

df_bar = pd.DataFrame(np.random.rand(10,4), 
                      columns=list('ABCD'))
df_bar.plot(kind='bar', cmap='viridis', title='multiple bar plot', alpha=0.7)
df_bar.plot.bar(cmap='viridis', title='multiple bar plot', alpha=0.7)

# %% słupkowy wierszowy

df_bar.plot.barh(cmap='viridis', title='multiple bar plot', alpha=0.7)

# %%  skumulowany
df_bar.plot.barh(cmap='viridis', title='multiple bar plot', alpha=0.7, stacked=True)

# %% histkogram

df= pd.DataFrame(np.random.rand(100000))

df.hist(bins=40)

df.plot(kind='hist', bins = 40)
# %%

df= pd.DataFrame(np.random.randn(100000))

df.hist(bins=100, color='red', alpha=0.5)

# %% 


df= pd.DataFrame({'mu_0_sigma_1':np.random.randn(100000),
                  'mu_1_sigma_2':2*np.random.randn(100000)+1,
                  'mu_8_sigma_3':3*np.random.randn(100000)+8})

df.plot.hist(bins=100, cmap='viridis', alpha=0.5, title='different normal distribution')


df['mu_8_sigma_3'].plot.hist(bins=100, cumulative=True, color='green', alpha=0.5)

# %%

df.hist(sharex=True, sharey=True, bins=100, color='green', alpha=0.5)