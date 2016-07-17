# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 09:49:32 2016
@author: Evgueni
"""

from random import randint
import numpy as np

#param input section:
it=10 #iteration cycles
nn=2  #N
tt=8   #T
aa=32 # a for P(a|b) 
bb=64 # b for P(a|b)


##get max and last for iterations in range
Lls=[]
Mls=[]
print('Iterated over', it, 'cycles.')
for i in range(it): #set # of iteration 1M is OK
    stream=[] #generate T register
    for i in range(tt): 
        stream.append(randint(1,10))    
       
    lastr=stream[-nn:]
    L=np.prod(lastr)
    Lls.append(L)
    stream.sort()
    maxr=stream[-nn:]
    M=np.prod(maxr)
    Mls.append(M)

#find mean part  
arL=np.array(Lls)
arM=np.array(Mls)
arD=arM-arL
print('Mean for N=', nn, 'T=', tt, 'is', arD.mean())
print('Std Dev for N=', nn, 'T=', tt, 'is', arD.std())

# P(a|b) part
arless=arD[arD<=bb]
armore=arless[arless>=aa]
prob=armore.size/arless.size
print('P(a|b) for a=', aa, 'b=', bb, 'is',  prob)






