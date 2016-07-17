# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 17:08:35 2016

@author: Evgueni
"""
import urllib
import pandas as pd

query=('https://data.medicare.gov/resource/r32h-32z5.json?$limit=50000&$offset=50000') #complications endpoint
query=('https://data.medicare.gov/resource/ppaw-hhm5.json?$limit=50000') #HAI endpoint
query=('https://data.medicare.gov/resource/rmgi-5fhi.json?$limit=50000&$offset=50000') #Patient survey endpoint

rawd=pd.read_json(query)
rawd.to_csv('filename.csv')
