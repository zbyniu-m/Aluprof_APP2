# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 22:45:52 2021

@author: USER
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# %% Zmiany procentowe

df = pd.read_csv('data/ten.csv', index_col=0)
df.columns=['Open','High','Low','Close','Volume']
clean_price = df[['Open', 'High', 'Low', 'Close']]
volume = df[['Volume']].copy()

# %% pct_change daily

df['Daily_change'] = df['Close'].pct_change()

# %% pct_change 5 days

df['Daily_change_5_days'] = df['Close'].pct_change(periods=5)

# %% pct_change close to open

df['Close_to_open'] = df[['Open','Close']].pct_change(axis=1).drop('Open',axis=1)

# %%

daily_changes = clean_price.pct_change()

# %% Korelacja

corr_matrix = clean_price.corr()

# %%
df['Open'].corr(df['Close'])

plt.matshow(corr_matrix)

sns.heatmap(corr_matrix)

# %% Rankingi

volume['Volume_Rank']=volume.rank(ascending=False)
volume = volume.sort_values(by='Volume_Rank', ascending=True)

# %%
top_10 = volume.nlargest(n=10, columns='Volume')

top_10['Volume'].plot(kind='bar', title='bar plot', cmap='viridis', alpha=0.5)

# %% by col

rank = clean_price.rank(method='first')

# %% by row

rank = clean_price.rank(method='first', axis=1)

# %% srednia kroczaca



"""
count() - number of non-null observations
sum()
mean()
median()
min()
max()
std()
var() - unbiased variance
skew() - skewness - 3 moment
kurt() - kurtosis - 4 moment
quantile()
apply()
cov()
corr()
"""

df = pd.read_csv('./data/ten.csv', index_col=0)
df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
clean_price = df[['Open', 'High', 'Low', 'Close']]

# %% Series
vol = df['Volume']
cum_vol = vol.cumsum()

cum_vol.plot()

# %% plot moving avarage
close = df['Close']

close_rol_avg = close.rolling(window=30).mean()
close.plot()
close_rol_avg.plot(style='k--')

# %% moving avarages
close.plot(color='black')
for i in [5, 8, 12, 60, 65, 70]:
    close_rol_avgs = close.rolling(window=i).mean()
    close_rol_avgs.plot(alpha=0.5)
    
# %% simple staregy
close.plot(color='black')
for i in [5]:
    close_rol_min = close.rolling(window=i).min()
    close_rol_min.plot()
    close_rol_max = close.rolling(window=i).max()
    close_rol_max.plot()
    
# %%
clean_price.rolling(window=20).mean().plot()
close.plot(color='black')

# %%
close.rolling(window=15).std().plot()
close.plot(color='black')

# %%
clean_price.rolling(window=20).mean().plot(subplots=True)

# %% własny wskaznik

xxx = close.rolling(window=10).apply(lambda x: (x - x.mean()).mean())
xxx.plot()