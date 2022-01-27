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


directories = ['ALL_MA_SFR_20', 'Pu_Np_20', 'Pu_Np_Am_20', 'TRU20']
titles = ['All TRU', 'NpPu', 'NpPuAm', 'TRU20']
fileTitles = ['ALL_MA_SFR_20', 'Pu_Np_20', 'Pu_Np_Am_20', 'TRU20']
rc['serpentVersion'] = '2.1.31'
cwd = os.getcwd()
last_bumats = {}
materials = {}
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
    
    plt.savefig(f'{fileTitle}_keff')
    plt.close()
    
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

    
    plt.savefig(f'{fileTitle}_CR')
    plt.close()
    materials[directory] = Code.read_bumat_files()
    
    plt.close()
#    os.chdir(directory)
 
    last_bumats[fileTitle] = Code.read_latest_bumat()[6]
    sum_of_TRU = 0
    for key in last_bumats[fileTitle]:
        if key > 93000:
            sum_of_TRU += last_bumats[fileTitle].get(key)
        else:
            last_bumats[fileTitle][key] = 0
    
    for key in last_bumats[fileTitle]:
        last_bumats[fileTitle][key] /= sum_of_TRU


plt.figure(figsize = (7,4))
plt.plot(np.array(materials['ALL_MA_SFR_20'][2])/365., materials['ALL_MA_SFR_20'][3][95241], label = 'All TRU')
plt.plot(np.array(materials['Pu_Np_Am_20'][2])/365., materials['Pu_Np_Am_20'][3][95241], label = 'NpPuAm')
plt.plot(np.array(materials['Pu_Np_20'][2])/365., materials['Pu_Np_20'][3][95241], label = 'NpPu')
#plt.plot(np.array(materials['TRU20'][2])/365., materials[3][94242], label = 'Pu')
plt.grid(which = 'both', snap = True)
plt.ylabel('Density (Atoms per barn cm)')
plt.xlabel('Years')
plt.legend()
    
    
plt.savefig(f'AmIsotopes')
#%%

os.chdir(cwd)

res = {'All TRU' : read('./ALL_MA_SFR_20/input9.inp_res.m').resdata,
       'NpPu' : read('./Pu_Np_20/input9.inp_res.m').resdata,
       'NpPuAm' : read('./Pu_Np_Am_20/input9.inp_res.m').resdata,
       'Pu' : read('./TRU20/input9.inp_res.m').resdata}

res = {'All TRU' : read('./ALL_MA_SFR_20/input0.inp_res.m').resdata,
       'NpPu' : read('./Pu_Np_20/input0.inp_res.m').resdata,
       'NpPuAm' : read('./Pu_Np_Am_20/input0.inp_res.m').resdata,
       'Pu' : read('./TRU20/input0.inp_res.m').resdata}


betas = {}
first_betas = {}
for key in res:
    x = res[key]
    betas[key] = np.mean(x['anaKeff'][:13, 4]/x['anaKeff'][:13, 0] * 100000)
    first_betas[directory] = np.mean(results[0].resdata['anaKeff'][:13, 4]/results[0].resdata['anaKeff'][:13, 0] * 100000)

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
dep = {}
#x = read('all_dep.m').materials['fuel']
activity = x.activity[-1, :]
for i in range(942389, 994250):
        try:
            activity -= x.activity[x.zai.index(i), :]
            print(i)
        except:
            pass
dep['All TRU'] = x

x = read('PuNpAm_dep.m').materials['fuel']
activity = x.activity[-1, :]

for i in range(930000, 960000):
        try:
            activity -= x.activity[x.zai.index(i), :]
            print(i)
        except:
            pass
dep['NpPuAm'] = x
activity = x.activity[-1, :]

x = read('Pu_dep.m').materials['fuel']
for i in range(942389, 944250):
        try:
            activity -= x.activity[x.zai.index(i), :]
            print(i)
        except:
            pass
dep['Pu'] = x
dep['LWR'] = read('LWR_waste.inp_dep.m').materials['fuel']

dep['All TRU'] = read('all_dep.m').materials['fuel']
dep['NpPuAm'] = read('PuNpAm_dep.m').materials['fuel']
dep['NpPu'] = read('NpPu3_dep.m')
dep['Pu'] = read('Pu_dep.m').materials['fuel']
dep['LWR'] = read('LWR_waste_dep.m').materials['fuel']

waste_per_energy = {}
TRU_per_energy = {}
DepU_per_energy = {}
FP_per_energy = {}

plt.figure(figsize = (7, 4))
for key in dep:
    
    try:
        x = dep[key].materials['fuel']
    except:
        x = dep[key]
    activity = x.activity[-1, :]
    
    energy = ((key == 'LWR') * 42 + (not key == 'LWR') * 70 ) * 9.31442e-3# [MWd/kg][kg/cm3][cm3]
    mass_waste = (x.mdens[-1,0] - x.mdens[13,0])/ 1000 #[kg]
    waste_per_energy[key] = mass_waste/energy *(365 * 1000) # kg/GWy
    
    DepU_per_energy[key] = 0
    FP_per_energy[key] = 0
    TRU_per_energy[key] = 0
    
    for i in range(len(x.names)-2):

        if x.zai[i] > 920000 and x.zai[i]< 930000:

            DepU_per_energy[key] +=  x.mdens[i,0]/energy *(365) * x.volume[0]
        elif x.zai[i]> 930000:
            TRU_per_energy[key] +=  x.mdens[i,0]/energy *(365)* x.volume[0]
        if x.zai[i]< 920000 and not i == 13:
            FP_per_energy[key] +=  x.mdens[i,0]/energy *(365)* x.volume[0]
    plt.loglog(x.days/365, (activity)/energy, '-' * (not key == 'LWR') + '--k'*(key == 'LWR'), label = key)
    
    
    #plt.loglog(x.days/365, (x.activity[-1, :])/x.activity[-1, 0], label = key) 
    #plt.loglog(x.days/365, (x.activity[-1, :])/(x.mdens[-1, :]- x.mdens[13, :])*x.volume, label = key) 
    
x = dep['All TRU']

'''
plt.loglog(x.days/365, (x.activity[-1, :])/(70*9.31442e-3*x.volume[0]),  '-k', label = 'total')
plt.loglog(x.days/365, (x.activity[158, :])/(70*9.31442e-3*x.volume[0]),  ':k', label = 'Cs137')
plt.loglog(x.days/365, (x.activity[200, :])/(70*9.31442e-3*x.volume[0]),  '*-k', label = 'Sm151')
plt.loglog(x.days/365, (x.activity[71, :])/(70*9.31442e-3*x.volume[0]),  '-.k', label = 'Tc99')
plt.loglog(x.days/365, (x.activity[156, :])/(70*9.31442e-3*x.volume[0]),  '--k', label = 'Cs135')
'''



#plt.loglog(x.days/365, (x.ingTox[1181, :])/(x.mdens[-1,:]-x.mdens[x.zai.index(80160), :])*x.volume, '--', label = 'Po210')

plt.xlim([1, 3*10**6])
plt.ylim([5*10**5 , 10**12])
plt.xlabel('Years')
plt.ylabel('Radioactivity [Bq/MWd]')
plt.title('Radioactivity per energy production')

plt.legend()
plt.grid(which = 'both')
plt.show()
    
#%%

plt.figure(figsize = (7, 3))
x = dep['LWR']

total = x.activity[-1, :]
activity_U = np.zeros(len(total))
activity_MA = np.zeros(len(total))
activity_FP = np.zeros(len(total))
activity_Pu = np.zeros(len(total))

for i in range(len(x.names)-2):

    if x.zai[i] > 920000 and x.zai[i]< 930000:
        activity_U += x.activity[i, :]
    elif x.zai[i] > 0 and x.zai[i]< 920000:
        activity_FP += x.activity[i, :]

    elif x.zai[i] > 930000:
        activity_MA += x.activity[i, :]

plt.loglog(x.days/365, (total)/energy, '-k', label = 'Total')
plt.loglog(x.days/365, (activity_U)/energy, ':k', label = 'Uranium')
plt.loglog(x.days/365, (activity_MA)/energy, '-.k', label = 'Transuranic elements')
plt.loglog(x.days/365, (activity_FP)/energy, '--k', label = 'Fission products')
    
    
plt.xlim([1, 3*10**6])
#plt.ylim([10**-2 , 10**4])
plt.xlabel('Years')
plt.ylabel('Radioactivity [Bq/MWd]')
plt.title('LWR SNF radioactivity')
plt.legend()
plt.grid(which = 'both')
plt.savefig('LWR_activity')
plt.show()

#%%
x = dep['All TRU']
largest_activity = []
activity = x.activity[0:len(x.names)-1, :]

for i in range(len(x.burnup)):
    a_step = list(activity[:,i])
    max_a = 0.
    for a in a_step:
        if a > max_a:
            max_a = a
    
    largest_activity.append([int(x.days[i]/365), x.names[a_step.index(max_a)]])


#%%

plt.figure()

N_TRU_data = {'All TRU' : np.load('ALL_MA_SFR_20/N_external_TRU.npy', allow_pickle=True),
              'NpPu' : np.load('./Pu_Np_20/N_external_TRU.npy', allow_pickle=True),
              'NpPuAm' : np.load('./Pu_Np_Am_20/N_external_TRU.npy', allow_pickle=True),
              'Pu' : np.load('./TRU20/N_external_TRU.npy', allow_pickle=True)}

N_TRU_data = {'All TRU' : np.load('ugh/ALL_MA_SFR_20/N_external_TRU.npy', allow_pickle=True),
              'NpPu' : np.load('ugh/Pu_Np_20/N_external_TRU_PuNp.npy', allow_pickle=True),
              'NpPuAm' : np.load('ugh/Pu_Np_Am_20/N_external_TRU_PuNpAm.npy', allow_pickle=True),
              'Pu' : np.load('./N_external_TRU (2).npy', allow_pickle=True)}


dens = 9.31442
powdens = 27.44
#%%
for key in N_TRU_data:
    
    energy = ((key == 'LWR') * 42 + (not key == 'LWR') * 70 ) * 9.31442e-3# [MWd/kg][kg/cm3]
#    mass_waste = (x.mdens[-1,0] - x.mdens[13,0])/ 1000 #[kg]
#    waste_per_energy[key] = mass_waste/energy *(365 * 1000) # kg/GWy
    
    N_TRU_data[key] *= (365 * 1000)/(0.6022*energy)
    

#%%
plt.xlim([1, 20])
#plt.ylim([10**-2 , 10**4])
plt.xlabel('Cycle')
plt.ylabel('Flow of TRU (mol/W)')
plt.title('LWR SNF radioactivity')
plt.legend()
plt.grid(which = 'both')
plt.savefig('LWR_activity')
plt.show()