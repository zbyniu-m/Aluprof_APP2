# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 22:47:58 2021

@author: USER
"""

import numpy as np
import pandas as pd

#%%

df1 = pd.DataFrame(np.random.rand(10,4), columns=list('abcd'))
df2 = pd.DataFrame(np.random.rand(10,4), columns=list('abcd'))
df3 = pd.DataFrame(np.random.rand(10,4), columns=list('abcd'))
s =pd.Series(np.random.rand(10), name='x')

# %% concat

df = pd.concat([df1,df2,df3], ignore_index=True)

df = pd.concat([df1,df2,df3])
df = df.reset_index()

# %% different colmn names

df1 = pd.DataFrame(np.random.rand(10,4), columns=list('abcd'))
df2 = pd.DataFrame(np.random.rand(10,4), columns=list('efgh'))

df = pd.concat([df1,df2], axis=1) # łączenie z prawej strony 

# %% outer, inner

df1 = df1[::2]

df = pd.concat([df1,df2], axis=1, join='outer') # łączenie z prawej strony 

df = pd.concat([df1,df2], axis=1, join='inner') # łączenie z prawej strony


df = pd.concat([df2, s], axis=1)

#%% append 

df = df1.append(df2, ignore_index=True)

df=df1.append(df2).reset_index().drop('index', axis=1)

# %% merge

ten_pl = pd.read_csv('data/ten.csv', index_col=0)
plw_pl = pd.read_csv('data/plw.csv', index_col=0)

# %%

ten = ten_pl.copy()
plw = plw_pl.copy()

ten.columns = ['Open','High','Low','Close','Volume']
plw.columns = ['Open','High','Low','Close','Volume']

out=pd.merge(ten,plw, how='inner', left_index=True, right_index=True)


out=pd.merge(ten,plw, how='inner', left_index=True, right_index=True,
             suffixes=('_TEN','_PLW'))


out=pd.merge(ten,plw, how='outer', left_index=True, right_index=True,
             suffixes=('_TEN','_PLW'))

ten['Change'] = ten['Close']/ten['Close'].shift(1)-1
plw['Change'] = plw['Close']/plw['Close'].shift(1)-1

correlation_matrix = out.corr()

# %% merge po kluczu

d1 = {'date': ['2019-01-01', '2019-01-01', '2019-01-02', '2019-01-02'],
      'id_trans': ['0001', '0002', '0003', '0004'],
      'product_id': ['343', '523', '151', '522']}

d2 = {'date': ['2019-01-01', '2019-01-02', '2019-01-02', '2019-01-03'],
      'id_trans': ['0001', '0002', '0003', '0004'],
      'price': ['99', '149', '59', '199']}

left = pd.DataFrame(d1)
right = pd.DataFrame(d2)

# %% inner
df_inner = pd.merge(left, right, how='inner', on=['date', 'id_trans'])

# %% outer
df_outer = pd.merge(left, right, how='outer', on=['date', 'id_trans'])

# %% left
df_left = pd.merge(left, right, how='left', on=['date', 'id_trans'])

# %% right
df_right = pd.merge(left, right, how='right', on=['date', 'id_trans'])



# %% join


left = pd.DataFrame(np.random.rand(10, 3),
                    index=pd.date_range('2019-01-01', periods=10),
                    columns=list('abc'))

right = pd.DataFrame(np.random.rand(10, 3),
                     index=pd.date_range('2019-01-04', periods=10),
                     columns=list('def'))

# %% left
left_join = left.join(right, how='left')

# %% right
right_join = left.join(right, how='right')

# %% inner
inner_join = left.join(right, how='inner')
# %% outer
outer_join = left.join(right, how='outer')
