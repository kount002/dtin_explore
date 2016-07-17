# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from sklearn import linear_model
#import matplotlib.pylab as plt



dataf='Historic_Secured_Property_Tax_Rolls.csv'
#dataf='property.csv'
df=pd.read_csv(dataf, header=0, dtype={'Closed Roll Exemption Type Code':str})

#q1
dff=df.groupby(['Property Class Code','Property Class Code Definition'])['Property Class Code'].count()
answ=dff.sort_values(ascending=False)
f=answ[0]/answ.sum()
print('Q1. The most common call type:', list(answ.index)[0])
print('Q1. Fraction is:', f, '\n')

#2
#remove prior assessments for multiples
dff=df.sort_values(['Block and Lot Number', 'Closed Roll Fiscal Year'])
dff=dff.drop_duplicates(['Block and Lot Number'], keep='last')
medv=dff['Closed Roll Assessed Improvement Value'].median()
print('Q2. Median value $', medv, '\n')

#3
dffmean=dff.groupby(['Neighborhood Code'])['Closed Roll Assessed Improvement Value'].mean()
diff=dffmean.max()-dffmean.min()
print('Q3. Difference between means by neighb', diff, '\n')

#4
#get years
#test=df[df.isin(dff)==False]

dfv=df[['Closed Roll Fiscal Year','Closed Roll Assessed Land Value']]
dfv=dfv[dfv['Closed Roll Assessed Land Value'].notnull()] #test this
dfv=dfv[dfv['Closed Roll Assessed Land Value']!=0] #remove zeros
arX=np.array(dfv['Closed Roll Fiscal Year'])
arY=np.array(dfv['Closed Roll Assessed Land Value'])
arY=np.log(arY)
lmod=linear_model.LinearRegression()
arX=arX.reshape(len(arX),1)
arY=arY.reshape(len(arY),1)
lmod.fit(arX, arY)
print('Q4. Estimated r is', lmod.coef_[0][0], '\n')

#5
dfl=dff[dff['Location'].notnull()]
codes=dfl['Neighborhood Code'].unique()
codes=codes.astype(str)
codes=codes[codes!='nan']
areals=[]
for i in codes:
    nb=dfl[dfl['Neighborhood Code']==i]
    loc=nb['Location']
    latls=[eval(x)[0] for x in loc]
    latls=[x for x in latls if x>35 and x<42]
    lonls=[eval(x)[1] for x in loc]
    lonls=[-x for x in lonls if x<-115 and x>-130]
    #print(max(lonls), min(lonls))
    
    #lonls=[x[1] for x in loc[0]]
    #lonls=[-x for x in lonls if x<-40]
    #latls=[x[0] for x in loc]
    #latls=[x for x in latls if x>10]
    
    area=111*np.std(latls)*np.pi*111*np.std(lonls)*np.cos(np.std(latls))
    tup=(i, area)
    areals.append(tup)

mv=max([x[1] for x in areals])
for tup in areals:
    if tup[1]==mv:
        print ('Q5. The largest district is ', tup, '\n')
        
#6
        
#remove prior assessments for multiples
#keep the fisrt
dff=df.sort_values(['Block and Lot Number', 'Closed Roll Fiscal Year'])
dff=dff.drop_duplicates(['Block and Lot Number'], keep='first')
#clean up
dfl=dff[dff['Number of Units'].notnull()]
dfl=dfl[dfl['Number of Units']>0]
dfl=dfl[dfl['Year Property Built'].notnull()]

before=dfl['Number of Units'][(dfl['Year Property Built']>1700) & (dfl['Year Property Built']<1950)].mean()
after=dfl['Number of Units'][(dfl['Year Property Built']>=1950) & (dfl['Year Property Built']<2016)].mean()

print('Q6. Difference in # units is', after-before, '\n')

#7
dff=df.sort_values(['Block and Lot Number', 'Closed Roll Fiscal Year'])
dff=dff.drop_duplicates(['Block and Lot Number'], keep='last')

dfl=dff[dff['Number of Units'].notnull()]
dfl=dfl[dfl['Number of Bedrooms'].notnull()]
dfl=dfl[dfl['Zipcode of Parcel'].notnull()]
dfl=dfl[(dfl['Number of Units']>0) & (dfl['Number of Bedrooms']>0)]

munit=dfl.groupby('Zipcode of Parcel')['Number of Units'].mean()
mbed=dfl.groupby('Zipcode of Parcel')['Number of Bedrooms'].mean()
bedunit=pd.concat([munit, mbed], axis=1, join='inner')
bedunit['Ratio']=bedunit['Number of Bedrooms']/bedunit['Number of Units']
maxrat=bedunit.Ratio.max()
print('Q7. Max ration of bedroom per unit by zip is', maxrat, '\n')

#8

dfl=dff[dff['Property Area in Square Feet'].notnull()]
dfl=dfl[dfl['Lot Area'].notnull()]
dfl=dfl[dfl['Zipcode of Parcel'].notnull()]
dfl=dfl[(dfl['Property Area in Square Feet']<1000000) & (dfl['Property Area in Square Feet']>100) & (dfl['Lot Area']>100) & (dfl['Zipcode of Parcel']>0)]
dfl['BURatio']=dfl['Property Area in Square Feet']/dfl['Lot Area']
burat=dfl.groupby('Zipcode of Parcel')['BURatio'].mean().max()
print('Q8. Largest build-up ratio is', burat, '\n')









