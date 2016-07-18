# -*- coding: utf-8 -*-

'''
Run retrive.py to save all data files locally
Available as a separate script


import urllib
import pandas as pd

query=('https://data.medicare.gov/resource/r32h-32z5.json?$limit=50000&$offset=50000') #complications endpoint
query=('https://data.medicare.gov/resource/ppaw-hhm5.json?$limit=50000') #HAI endpoint
query=('https://data.medicare.gov/resource/rmgi-5fhi.json?$limit=50000&$offset=50000') #Patient survey endpoint

rawd=pd.read_json(query)
rawd.to_csv('filename.csv')

'''


#import matplotlib
#matplotlib.use('Agg') #need to comment if want to see plots in the spyder
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import seaborn as sns
#import pickle
#import sys
#import os
#from bokeh.plotting import figure, output_file, show
from mpl_toolkits.basemap import Basemap


def clean(df):
    df.replace('Not Applicable', np.nan, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    df.replace('Not Available', np.nan, inplace=True)
    df.dropna(axis=0, how='all', inplace=True)
    df=df.astype(float)
    return(df)


#load local data file
dataf='HOSArchive_Revised_FlatFiles_20151210/HCAHPS - Hospital.csv'
df=pd.read_csv(dataf, header=0, encoding='cp1252')

dfp=df.pivot(index='Provider ID', columns='HCAHPS Question', 
         values='HCAHPS Linear Mean Value')
         
dfp=clean(dfp) #clean table
         

#clean column names
names=list(dfp.columns)
mod=(lambda x: re.match(r'(.+)(\s-.+)', x).group(1))    
rename=[mod(x) for x in names]
dfp.columns=rename

#correlation matrix for overview
fig=sns.pairplot(dfp)
fig.savefig('matrix_review.png')

#heatmap of overview
plt.clf()
corr=dfp.corr()
cmap=sns.diverging_palette(120, 5, as_cmap=True)
sns.set(font_scale=1.6)
fig=sns.clustermap(corr, cmap=cmap, linewidths=.5)
plt.setp(fig.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
fig.savefig('clustermap.png')


#working on infection table
dataf='HOSArchive_Revised_FlatFiles_20151210/Healthcare Associated Infections - Hospital.csv'
dfi=pd.read_csv(dataf, header=0, encoding='cp1252')
dfip=dfi.pivot(index='Provider ID', columns='Measure Name', values='Score')

#remove columns in refuse
names=list(dfip.columns)
refuse=['Upper', 'Lower', 'Predicted']
mod=(lambda x: False if (set(x) & set(refuse)) else True)
names=list(filter(lambda x: mod(x.split(' ')), names))

#remove aggrage columns
moda=lambda x: re.match(r'.*\(.+\).*', x)
names=list(filter(lambda x: not moda(x), names))
dfip=dfip[names]
dfip=clean(dfip)
dfip['Incidence CDI']=dfip['C.diff Observed Cases']/dfip['C.diff Patient Days']

tab=pd.concat([dfp, dfip['Incidence CDI']], join='inner', axis=1)

#prep table for basemap

#make ID-ZIP table
dfi['tmp']='ZIP Code'
dfzp=dfi.pivot_table(index='Provider ID', columns='tmp', values='ZIP Code', aggfunc=np.min)

#make ID-CDI_ZIP table
tbsl=tab['Incidence CDI']
tbzp=pd.concat([tbsl, dfzp], join='inner', axis=1)
tbzp.dropna(inplace=True)

citi=pd.read_csv('zip_codes_states.csv', header=0)
tbps=pd.merge(tbzp, citi, left_on='ZIP Code', right_on='zip_code', how='inner')


#basemap 
plt.clf()
plt.figure(1, figsize=(24,16))
m = Basemap(projection='merc',
             llcrnrlat=24, urcrnrlat=50,
             llcrnrlon=-128, urcrnrlon=-60,
             lat_ts=0, resolution='c')
m.fillcontinents(color='silver',lake_color='#000000') # dark grey land, black lakes
m.drawmapboundary(fill_color='#000000')                # black background
m.drawcountries(linewidth=0.1, color="w")              # thin white line for country border
         
#plot data
mxy = m(tbps["longitude"].tolist(), 
         tbps["latitude"].tolist())
         
#size=lambda x: tbps.ix['Incidence CDI']
size=tbps["Incidence CDI"].tolist()
size=[x*400000 for x in size]
m.scatter(mxy[0], mxy[1], s=size, c="#1292db", lw=0, alpha=0.20, zorder=5)
m.scatter(mxy[0], mxy[1], s=23, c="m", lw=0, alpha=0.4, zorder=5)

plt.savefig('CDI_map.png')

#analyse histogram of CDI
plt.close()
plt.figure(1, figsize=(6,6))
x=np.array(dfip['Incidence CDI'].dropna())
sns.distplot(x, bins=40)
plt.savefig('incid_hist.png')

