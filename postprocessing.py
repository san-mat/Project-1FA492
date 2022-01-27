# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 13:57:04 2021

@author: matti
"""
import numpy as np
import Code
import os
from serpentTools import *
from serpentTools.settings import rc
import matplotlib.pyplot as plt


directory = '.'
rc['serpentVersion'] = '2.1.31'
os.chdir(directory)
    
print(f'Current directory: {os.curdir}')
    
res_files = []
results = []
for filename in os.listdir():
    if 'res' in filename:
        res_files.append(filename)
        results.append(read(filename))
dep_files = []
materials = Code.read_bumat_files()
    
#    results[0].plot('conversionRatio')
    
    #waste = np.load('waste.npy', allow_pickle = True)
fig = plt.figure()
#fig, ax = plt.figure()
ax = results[1].plot('burnDays', {'anaKeff' : '$k_{eff}$'})
ax =results[2].plot('burnDays', {'anaKeff'}, ax = ax)
ax =results[3].plot('burnDays', {'anaKeff'}, ax = ax)
ax =results[5].plot('burnDays', {'anaKeff'}, ax = ax)
ax =results[7].plot('burnDays', {'anaKeff'}, ax = ax)
#ax =results[8].plot('burnup', {'anaKeff' : 'sista'}, ax = ax)
#%%
materials = Code.read_bumat_files()
plt.figure()
plt.semilogy(materials[2], materials[3][94239])
plt.semilogy(materials[2], materials[3][94240])
plt.semilogy(materials[2], materials[3][94241])
plt.semilogy(materials[2], materials[3][94242])