# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 15:04:07 2016
@author: Evgueni
"""
from random import randint
import numpy as np

#param section
'''
Use pset=0 for T10 set, use pset=1 for T1024 set
'''
pset=1
it=100000 # iterations

if not pset:
    tt=10 # T moves
    mm=10 # mod modulo
    aa=5 # a for P(a|b)
    bb=7  # b for P(a|b)
else:
    tt=1024 # T moves
    mm=1024 # mod modulo
    aa=23  # a for P(a|b)
    bb=29  # b for P(a|b)


#move dic
moves={0:[4,6], 1:[6,8], 2:[7,9], 3:[4,8], 4:[3,9,0], 6:[1,7,0], 7:[2,6], 8:[1,3], 9:[4,2]}

print ('Change pset value in body \n', 'Use pset=0 for T10 set, use pset=1 for T1024 set')
print('Iterated over', it, 'cycles.')
Sl=[]
for i in range(it):
    key=0
    stream=[]
    for i in range(tt):
        #for key in moves.keys():
        ind=len(moves[key])-1 # #of steps
        pos=randint(0,ind)    # chose random step
        #print(key, pos)
        key=moves[key][pos]
        stream.append(key) 
    #print(stream)
    Sl.append(sum(stream))
    Ml=[x%mm for x in Sl]
arS=np.array(Sl)
arM=np.array(Ml)

print('Mean for T=', tt, 'mod', mm, 'is', arM.mean())
print('Std Dev for T=', tt, 'mod', mm, 'is', arM.std())

# P(a|b)

arB=arS%bb #residuals for b
arBb=arB==0 #bool divisible by b
arSf=arS[arBb] #extract divisible b #count all b events use size
arA=arSf%aa #residual for a
arAf=arA[arA==0]
if arSf.size!=0:
    prob=arAf.size/arSf.size
else:
    prob=0

print('P(a|b) for a=', aa, 'b=', bb, 'is',  prob)
