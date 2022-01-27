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


directories = ['SFR_50TRU', 'SFR_75TRU','SFR_TRU']
titles = ['10% Pu, 10% U235', '15% Pu, 5% U235', '20% Pu']
fileTitles = ['SFR_50TRU', 'SFR_75TRU', 'SFR_TRU']
rc['serpentVersion'] = '2.1.31'
cwd = os.getcwd()
last_bumats = {}

#%%
for i, directory in enumerate(directories):
    os.chdir(cwd)
    os.chdir(directory)
    title = titles[i]
    fileTitle = fileTitles[i]
    print(f'Current directory: {os.curdir}')
        
    res_files = []
    results = []
    for filename in os.listdir():
        if 'res' in filename and 'input' in filename:
            res_files.append(filename)
            result = read(filename)
            result.resdata['burnDays'] /= 365
            results.append(result)
    
    dep_files = []
       
    #    results[0].plot('conversionRatio')
        
        #waste = np.load('waste.npy', allow_pickle = True)
    fig = plt.figure()
    #fig, ax = plt.figure()
    ax = results[0].plot('burnDays', {'anaKeff' : '1:st cycle'})
    ax =results[1].plot('burnDays', {'anaKeff' : '2:nd cycle'}, ax = ax)
    ax =results[2].plot('burnDays', {'anaKeff' : '3:rd cycle'}, ax = ax)
    ax =results[7].plot('burnDays', {'anaKeff' : '8:th cycle'}, ax = ax)
    ax =results[8].plot('burnDays', {'anaKeff' : '9:th cycle'}, ax = ax)
    ax =results[9].plot('burnDays', {'anaKeff'  : '10:th cycle '}, ax = ax)
    plt.grid()
    plt.xlabel('Years')
    plt.ylabel('$k_{inf}$')
    plt.title(title)
    ax.set_xlim([0, results[0].resdata['burnDays'][13][0]])
    ax.set_ylim([1, 2])
    plt.grid(which = 'minor')
    
    os.chdir(cwd)
    plt.savefig(f'{fileTitle}_keff')
    plt.close()
    os.chdir(directory)
    
    fig = plt.figure()
    #fig, ax = plt.figure()
    ax = results[0].plot('burnDays', {'conversionRatio' : '1:st cycle'})
    ax =results[1].plot('burnDays', {'conversionRatio' : '2:nd cycle'}, ax = ax)
    ax =results[2].plot('burnDays', {'conversionRatio' : '3:rd cycle'}, ax = ax)
    ax =results[7].plot('burnDays', {'conversionRatio' : '8:th cycle'}, ax = ax)
    ax =results[8].plot('burnDays', {'conversionRatio' : '9:th cycle'}, ax = ax)
    ax =results[9].plot('burnDays', {'conversionRatio'  : '10:th cycle '}, ax = ax)
    plt.xlabel('Years')
    plt.ylabel('Conversion ratio')
    plt.grid()
    #plt.title(title)
    ax.set_xlim([0, results[0].resdata['burnDays'][13][0]])
    ax.set_ylim([0, 1.5])
    plt.grid(which = 'minor')

    
    os.chdir(cwd)
    plt.savefig(f'{fileTitle}_CR')
    plt.close()
    os.chdir(directory)
    materials = Code.read_bumat_files()
    plt.figure(figsize = (7,4))
    plt.semilogy(np.array(materials[2])/365., materials[3][92235], label = 'U-235')
    plt.semilogy(np.array(materials[2])/365., materials[3][94239], label = 'Pu-239')
    plt.semilogy(np.array(materials[2])/365., materials[3][94240], label = 'Pu-240')
    plt.semilogy(np.array(materials[2])/365., materials[3][94241], label = 'Pu-241')
    plt.semilogy(np.array(materials[2])/365., materials[3][94242], label = 'Pu-242')
    plt.grid(which = 'both', snap = True)
    plt.ylabel('Density (Atoms per barn cm)')
    plt.xlabel('Years')
    plt.legend()
    
    
    
    
    os.chdir(cwd)
    plt.savefig(f'{fileTitle}_PuIsotupes')
    plt.close()
    os.chdir(directory)
 
    last_bumats[fileTitle] = Code.read_latest_bumat()[6]
    sum_of_TRU = 0
    for key in last_bumats[fileTitle]:
        if key > 93000:
            sum_of_TRU += last_bumats[fileTitle].get(key)
        else:
            last_bumats[fileTitle][key] = 0
    
    for key in last_bumats[fileTitle]:
        last_bumats[fileTitle][key] /= sum_of_TRU
#%%


N_TRU_data = {}
N_235_data = {}
for i, directory in enumerate(directories):
    os.chdir(cwd)
    os.chdir(directory)
    
    N_TRU_data[fileTitles[i]] = np.load('N_external_TRU.npy', allow_pickle=True)
    N_235_data[fileTitles[i]] = np.load('N_external_U235.npy', allow_pickle=True)
    # N_235_data = np.load('N_external_U235.npy', allow_pickle=True)
    
#%%

    
    