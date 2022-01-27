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


directories = ['SFR_75TRU','TRU20',
               'TRU25',
               'TRU30', 'TRU35']
titles = ['15% Pu', '20% Pu', '25% Pu', '30% Pu', '35% Pu']
fileTitles = ['TRU15', 'TRU20', 'TRU25', 'TRU30', 'TRU35']
rc['serpentVersion'] = '2.1.31'
cwd = os.getcwd()
last_bumats = {}
betas = {}
first_betas = {}
#%%
for i, directory in enumerate(directories):
    os.chdir(cwd)
    os.chdir(directory)
    title = titles[i]
    dep_files = []
    deps = []

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
        if 'dep.m' in filename and 'input' in filename:
            dep_files.append(filename)
            dep = read(filename)
            deps.append(dep)
    
    
       
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
        
    betas[directory] = np.mean(results[9].resdata['anaKeff'][:13, 4]/results[9].resdata['anaKeff'][:13, 0] * 100000)
    first_betas[directory] = np.mean(results[0].resdata['anaKeff'][:13, 4]/results[0].resdata['anaKeff'][:13, 0] * 100000)


#%%

finals = []
N_TRU_data = {}
N_235_data = {}
for i, directory in enumerate(directories):
    os.chdir(cwd)
    os.chdir(directory)
    
    finals.append(read(os.listdir()[os.listdir().index('final.inp_dep.m')]))
    N_TRU_data[fileTitles[i]] = np.load('N_external_TRU.npy', allow_pickle=True)
    N_235_data[fileTitles[i]] = np.load('N_external_U235.npy', allow_pickle=True)
    # N_235_data = np.load('N_external_U235.npy', allow_pickle=True)
    
for key in N_TRU_data:
    
    energy = ((key == 'LWR') * 42 + (not key == 'LWR') * 70 ) * 9.31442e-3# [MWd/kg][kg/cm3][cm3]
    #mass_waste = (result.mdens[-1,0] - result.mdens[13,0])/ 1000 #[kg]
    #waste_per_energy[key] = mass_waste/energy *(365 * 1000) # kg/GWy
    
    N_TRU_data[key] *= (365 * 1000)/(0.6022*energy)
    
#%%
plt.figure()
for final in finals:
    total = final.materials['total']
    plt.loglog(final.days/365, final.materials['total'].activity[-1,:], label = title) 
    
plt.grid(which = 'both', snap = True)
plt.ylabel('Activity (Bq)')
plt.xlabel('Years')
plt.legend()
plt.savefig('activity')