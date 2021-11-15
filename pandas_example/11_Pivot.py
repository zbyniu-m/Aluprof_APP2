# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 22:19:24 2021

@author: USER
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()


# %%
tit = sns.load_dataset('titanic')

# %% grouping by sex and ploting

tit.groupby('sex').size().plot(kind='bar', alpha=0.5) # ilosc elementow
tit.groupby(['sex','survived']).size().plot(kind='bar', alpha=0.5) # ilosc elementow

# %% grouping by classes

tit.groupby('class').size().plot(kind='bar', alpha=0.5)
tit.groupby('class').mean()['survived'].plot(kind='bar')

r = pd.pivot_table(data=tit, values='survived', index='sex', columns='class', aggfunc='count')

# %% making variable age categorical and gouping by age

tit['age_bin'] = pd.cut(x=tit['age'], bins=[0,18,80])

pv = pd.pivot_table(data=tit, values='survived', index='age_bin', columns='class',aggfunc='count')

# %% making subplots

fig, ax = plt.subplots(1, 2, sharey=True)
tit.groupby(['sex','survived']).size()['male'].plot(ax=ax[0], kind='bar')
tit.groupby(['sex','survived']).size()['female'].plot(ax=ax[1], kind='bar')
ax[0].legend('male')
ax[1].legend('female')

# %% pivoting table

r = pd.pivot_table(data=tit, values='age', index='survived', columns='sex', aggfunc='count')
r.plot(subplots=True, kind='bar', sharey=True, layout=(1,2))

# %% 

pv2 = pd.pivot_table(data=tit, index='sex', columns='class', aggfunc={'survived': sum, 'fare':'mean'})


# %%

url = ('https://archive.ics.uci.edu/ml/machine-learning-databases/00492/'
       'Metro_Interstate_Traffic_Volume.csv.gz')

# %%
metro = pd.read_csv(url, compression='gzip', parse_dates=True,
                    index_col='date_time')

metro = metro.loc['2016-01-01':]

# %%
traffic = metro.iloc[:, -1:]
traffic.plot()
tr = traffic.resample('M').sum()
tr.plot()

# %%
metro.pivot_table(values='traffic_volume', index='weather_main').\
      plot(kind='bar')

metro.groupby('holiday').mean()['traffic_volume'].plot(kind='bar')

# %%

tips = sns.load_dataset('tips')

# %%
tips.pivot_table(values='tip', index='sex', columns='day', aggfunc='mean')
pv = tips.pivot_table(values=['total_bill', 'tip'], index='sex', columns='day',
                 aggfunc='mean')

pv = tips.pivot_table(values='tip', index='sex', columns=['smoker', 'day'])

# %%
tips.pivot_table(values='tip', index='sex', columns='day', aggfunc='mean').\
     plot(kind='bar', cmap='viridis', alpha=0.5)

tips.pivot_table(values='total_bill', index='sex', columns='day',
                 aggfunc='mean').plot(kind='bar', cmap='viridis', alpha=0.5)

tips.pivot_table(values='total_bill', index='day', columns='size',
                 aggfunc='mean').plot(kind='bar', cmap='viridis', alpha=0.5)

tips.pivot_table(values='total_bill', index='time', columns='day',
                 aggfunc='mean').plot(kind='bar', cmap='viridis', alpha=0.5)


vals = tips[['total_bill', 'tip', 'size']]
vals.corr()