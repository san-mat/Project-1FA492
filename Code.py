
"""
Created on %(date)s

@author: %Mattias Sandnabba
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import re

def __init__(self):
    pass
	

"""
read_res_file()

Return dictionary of specified variables
"""

def read_res_file(filename, important_variables = None, np_arrays = True):
    
   values = {}
   test_line = []
   file = open(filename, 'r')
   
   if important_variables is None: # Read all
       for line in file:
           line = line.split(' ')
           
           if line[0] == line[0].upper() and bool(line[0].strip()) and not line[0].startswith('%'):
               key = line[0]
               data = []
               for token in line:
                   try:
                       data.append(float(token))
                   except:
                       pass
               try:
                   # Try to append to existing list
                   values[key].append(data)
               except:
                   # Create new entry in values
                   values = {**values, key: [data]} 
       
   else:
       for line in file:
           line = line.split(' ')
           
           if line[0] in important_variables:
               key = line[0]
               data = []
               for token in line:
                   try:
                       data.append(float(token))
                   except:
                       pass
               try:
                   # Try to append to existing list
                   values[key].append(data)
               except:
                   # Create new entry in values
                   values = {**values, key: [data]} 
       
   if np_arrays == True: # convert data to np arrays
       for value_name in values:
           values[value_name] = np.array(values[value_name])
   file.close()
   return values

"""
Read a bumat file

Return burnup, days and material dictionaries with name and ZA keys
"""
def read_bumat_file(filename):
    file = open(filename, 'r')
    days = 0
    burnup = 0
    materials_name = {}
    materials_ZA = {}  
    temp = 0
    dens = 0
    vol = 0
    # Find the days and burnup from bumap file
    for line in file:
        if '% Material' in line:
            s = re.split('\(| ', line)
            burnup = float(s[4])
            days = float(s[7])
        if 'mat ' in line:
            s = line.split()
            dens = float(s[2])
            vol = float(s[4])
        else:
            try:
                
                name = line.split()[0]
                ZA = int(name.split('.')[0])
                temp = name.split('.')[1]
                rel_dens = float(line.split()[1])
                materials_name = {**materials_name, name: rel_dens}
                materials_ZA = {**materials_ZA, ZA: rel_dens}
            except: # Empty string, skip
                pass #print(line)
    return burnup, days, temp, dens, vol, materials_name, materials_ZA

def sorting_key(str):
    if '.bumat' in str:
        try:
            nb = re.split('waste|input|.inp.bumat', str)
            return ('input' in str)*1000000 + int(nb[1])*1000 + int(nb[2])
        except:
            pass
    return -len(str)

"""
Read latest bumat file (highest index)


"""
def read_latest_bumat(dirname = '.'):
    bumat_files = []
    for filename in os.listdir(dirname):
        if '.bumat' in filename and 'input' in filename: 
            bumat_files.append(os.path.join(dirname,filename))
    
    bumat_files = sorted(bumat_files, key = sorting_key) # Sort from last to first
    return read_bumat_file(bumat_files[-1])

def read_first_bumat(dirname = '.'):
    bumat_files = []
    for filename in os.listdir(dirname):
        if '.bumat' in filename and 'input' in filename: 
            bumat_files.append(os.path.join(dirname,filename))
    
    bumat_files = sorted(bumat_files, key = sorting_key) # Sort from last to first
    return read_bumat_file(bumat_files[0])


"""
Read all .bumat (burnup material output files) in a folder

Return lists burnup, days and material density dictionaries
(For plotting)
"""

def read_bumat_files(dirname = '.', np_arrays = True, only_input = True):
    
    bumat_files = []
    for filename in os.listdir(dirname):
        if '.bumat' in filename: 
            #bumat_files.append(path + filename)
            if only_input == False:
                bumat_files.append(os.path.join(dirname,filename))
            elif 'input' in filename:
                bumat_files.append(os.path.join(dirname,filename))
    
    bumat_files = sorted(bumat_files, key = sorting_key) # Sort from first to last
    
    materials_list = {}
    days_list = []
    cumulative_days = []
    burnup_list = []
    for filename in bumat_files:
        file = open(filename)
        
        # Find the days and burnup from bumat file
        for line in file:
            if '% Material' in line:
                s = re.split('\(| ', line)
                burnup_list.append(float(s[4]))
                days_list.append(float(s[7]))
                break
        mat = {}    
        for i, line in enumerate(file):
            if i > 5: # Skip rows
                try:
                    s = line.split()
                    ZA = int(s[0].split('.')[0])
                    rel_dens = float(s[1])
                    try:
                        materials_list[s[0]].append(float(s[1]))
                        materials_list[ZA].append(rel_dens)
                    except KeyError:
                        #Create new key if material is not listed
                        materials_list = {**materials_list, s[0]: [rel_dens]}
                        materials_list = {**materials_list, ZA: [rel_dens]}
                except Exception as e:
                    print(e)
    last_cycle_end = 0   
    cumulative_days = [0]
    for i in range(1,len(days_list)):
        if days_list[i] == 0:
            last_cycle_end += days_list[i-1]
        cumulative_days.append(days_list[i] + last_cycle_end)
    return burnup_list, days_list, cumulative_days, materials_list
test = read_bumat_files()
"""
Give externally supplied TRU composition
"""
def external_TRU(recycle_limit):
    BU, days, temp, dens, vol, mats_name, mats_ZA = read_bumat_file('SNF_LWR.txt')
    
    keys = list(mats_ZA.keys())
    for key in keys:
        if key < recycle_limit[0] or key > recycle_limit[1]:
            del mats_ZA[key]
    
    # Normalize
    sum_of_mats = 0
    for key in mats_ZA:
        sum_of_mats += mats_ZA.get(key)
    for key in mats_ZA:
        mats_ZA[key] /= sum_of_mats
    
    return mats_ZA


"""
Return the number density of actinides in the original composition
Unit (barn cm)^-1
"""
def initial_number_density(dirname = '.'):
    try:
        BU, days, temp, dens, vol, mats_name, mats_ZA = read_first_bumat()
        #Normalize fractions
        sum_of_mats = 0
        for key in mats_ZA:
            sum_of_mats += mats_ZA.get(key)
        for key in mats_ZA:
            mats_ZA[key] /= sum_of_mats
    
        # Find actinide fraction
        sum_of_act = 0
        for key in mats_ZA:
            if key > 92000:
                sum_of_act += mats_ZA.get(key)
        return dens * sum_of_act
    except:
        return 0.02347
"""

"""
def recycle(filename = None, TRU_enr = None, U_enr = None,
            recycle_isotopes = range(94000, 95000), 
            Temp = None, exclude_isotopes = [],
            savefile = 'fuel.txt', wastefile = 'FR_SNF.txt'):
    
    # By default, read highest index bumat file
    if filename is None:
        BU, days, temp, dens, vol, mats_name, fuel_ZA = read_latest_bumat()
    else:
        BU, days, temp, dens, vol, mats_name, fuel_ZA = read_bumat_file(filename)
    
    if not Temp is None:
        temp = Temp
    
    line_dens = 1e24*vol*dens
    print(fuel_ZA)
    
    #Normalize fractions
    sum_of_mats = 0
    for key in fuel_ZA:
        sum_of_mats += fuel_ZA.get(key)
    for key in fuel_ZA:
        fuel_ZA[key] /= sum_of_mats
    
    TRU_multiplier = 1
    U_multiplier = 1
    waste_ZA = {}
    
    # Keep only actinides
    keys = list(fuel_ZA.keys())
    for key in keys:
        if key < 92000:
            waste_ZA = {**waste_ZA, key : fuel_ZA.get(key)} # Add to waste
            del fuel_ZA[key]
            print(key)
    
    # Discard MA:s outside recycle limit
    keys = list(fuel_ZA.keys())
    for key in keys:
        if (not key in recycle_isotopes or key in exclude_isotopes) and key > 93000:
            waste_ZA = {**waste_ZA, key : fuel_ZA.get(key)} # Add to waste
            del fuel_ZA[key]
    
    #Normalize fractions
    sum_of_mats = 0
    for key in fuel_ZA:
        sum_of_mats += fuel_ZA.get(key)
        
    for key in fuel_ZA:
        fuel_ZA[key] /= sum_of_mats
    print(sum_of_mats)
    # Atoms [1/(b*cm)] in waste and fuel
    
    dens_fuel = dens*sum_of_mats
    dens_act = dens_fuel
        
    
    # Enrichment to TRU atomic percentage
    N_external_TRU = 0
    if not TRU_enr is None:
        sum_of_TRU = 0
        for key in fuel_ZA:
            if key in recycle_isotopes:
                sum_of_TRU += fuel_ZA.get(key)
        TRU_multiplier = TRU_enr/sum_of_TRU
        for key in fuel_ZA:
            ext_TRU = external_TRU([min(recycle_isotopes), max(recycle_isotopes)])
            if key in recycle_isotopes:
                fuel_ZA[key] *= min(dens_fuel/initial_number_density(),TRU_multiplier) # Reuse TRU from fuel
                try:
                    fuel_ZA[key] += max(0, TRU_enr - sum_of_TRU*dens_fuel/initial_number_density())*ext_TRU.get(key)
                except TypeError: # The isotope does not exist in SNF_LWR. This is fine
                    pass
            elif key > 92000 and key < 93000:
                waste_ZA = {**waste_ZA, key : (TRU_enr - sum_of_TRU)*fuel_ZA.get(key)*sum_of_mats}
                fuel_ZA[key] *= (1 - TRU_enr)/(1 - sum_of_TRU)

                
        N_external_TRU = (TRU_enr*initial_number_density() - sum_of_TRU*dens_fuel)
            
    N_external_U235 = 0    
    # Enrichment of U atomic percentage
    print(fuel_ZA)
    if not U_enr is None:
        U235 = 0
        U238 = 0
        for key in fuel_ZA:
            if key <= 92236:
                U235 += fuel_ZA.get(key)
            elif key < 93000:
                U238 += fuel_ZA.get(key)
        try:
            U_multiplier = U_enr/U235/(1-TRU_enr)
        except:
            U_multiplier = 0
        for key in fuel_ZA:
            if key > 92000 and key <= 92236:
                fuel_ZA[key] *= min(U_multiplier, dens_fuel/initial_number_density())
            if key > 92236 and key < 94000:
                try:    
                    fuel_ZA[key] *= (1 - U_enr -TRU_enr)/(U238)
                except ZeroDivisionError:
                    pass
        
        fuel_ZA[92235] += max(0, (U_enr- U235*dens_fuel/initial_number_density()))    
        N_external_U235 = (U_enr*initial_number_density()/(1-TRU_enr) - U235*dens_fuel)
    
    # density proportional to average mass number
    densities = {'9c'  : -10.66, 
                 '12c' : -10.55, 
                 '15c' : -10.42, 
                 '18c' : -10.28} # density of UO2 (g/cm3)
    
    A = 0 # Average mass number
    for key in fuel_ZA:
        A += (key % 1000) * fuel_ZA.get(key)
    density = densities.get(temp)*((A + 32)/(238 + 32))
    print(A)
    print(dens_fuel)
    print(initial_number_density())
    # Write fuel file to include
    lines = [f'mat fuel {density} burn 1\n\n\n', f'8016.{temp}   2\n']
    for key in fuel_ZA:
        lines.append(f'{key}.{temp}   {fuel_ZA.get(key)}\n')
    file = open(savefile, 'w')
    file.writelines(lines)
    file.close()
    
    # Normalize waste file
    sum_of_waste = 0
    for key in waste_ZA:
        sum_of_waste += waste_ZA.get(key)
    for key in waste_ZA:
        waste_ZA[key] /= sum_of_waste
    dens_waste = sum_of_waste * dens
    waste_ZA = {**waste_ZA, 'dens' : dens_waste}
    
    # Write waste file to include
    lines = [f'mat fuel {dens_waste} burn 1\n\n\n']
    for key in waste_ZA:
        try:
            lines.append(f'{int(key)}.{temp}   {waste_ZA.get(key)}\n')
        except:
            pass
    file = open(wastefile, 'w')
    file.writelines(lines)
    file.close()
    
    sum_of_mats = 0
    for key in fuel_ZA:
        sum_of_mats += fuel_ZA.get(key)
    print(sum_of_mats)
    # Return nb. of atoms per barn*cm
    
    sum_of_TRU = 0
    for key in fuel_ZA:
        if key in recycle_isotopes:
            sum_of_TRU += fuel_ZA.get(key)
    print(sum_of_TRU)
    
    return N_external_TRU, N_external_U235, waste_ZA, fuel_ZA
test = recycle(TRU_enr = .20)
def add_waste(last_waste_file, current_waste_file, wastefile):
    last = read_bumat_file(last_waste_file)
    last_dens = last[3]
    last_waste = last[6]
    current = read_bumat_file(current_waste_file)
    current_dens = current[3]
    current_waste = current[6]
    vol = current[4]
    
    for key in current_waste:
        current_waste[key] = current_waste[key]*current_dens + last_waste.get(key, 0)*last_dens
    # Normalize waste file
    sum_of_waste = 0
    for key in current_waste:
        sum_of_waste += current_waste.get(key)
    for key in current_waste:
        current_waste[key] /= sum_of_waste
        
    # Write waste file to include
    lines = [f'mat waste {current_dens + last_dens} vol {vol} burn 1\n\n\n']
    for key in current_waste:
        try:
            lines.append(f'{int(key)}.{current[2]}   {current_waste.get(key)}\n')
        except:
            pass
    file = open(wastefile, 'w')
    file.writelines(lines)
    file.close()
    
def depsteps(filename = 'input.inp'):
    steps = 1 # One depletion step is at time = 0
    with open(filename) as file:
        file = file.readlines()
        for i, line in enumerate(file):
            if line.startswith('dep '):
                i += 1
                while i < len(file):
                    l = file[i].strip()
                    try:
                        float(l.split('%')[0]) # Handle comments
                        steps += 1
                        i += 1
                    except ValueError:
                        if l.startswith('%') or not l: # Empty or comment
                            i += 1
                        else:
                            break # End of dep card
            elif line.startswith('include '):
                try:
                    steps += depsteps(re.split(' |%', line)[1].strip()) - 1 # Check inclusion for depletion steps
                except FileNotFoundError:
                    pass
    return steps

def total_inventory(current_step = None):
    fuel_files = []
    waste_files = []
    final_files = []
    if current_step is None:
        for filename in os.listdir():
            if '.bumat' in filename:
                if 'input' in filename:
                    fuel_files.append(filename)
                else:
                    waste_files.append(filename)
        fuel_files = sorted(fuel_files, key = sorting_key)
        waste_files = sorted(waste_files, key = sorting_key)
        i= 0
        while True:
            try:
                files = []
                for filename in waste_files:
                    if f'waste{i}' in filename:
                        files.append(filename)
                final_files.append(files[-1])
                i += 1
            except IndexError:
                break
              
    else:
        for filename in os.listdir():
            if '.bumat' in filename:
                if f'input{current_step}' in filename:
                    fuel_files.append(filename)
                elif 'waste' in filename:
                    waste_files.append(filename)
        fuel_files = sorted(fuel_files, key = sorting_key)
        waste_files = sorted(waste_files, key = sorting_key)
        i= 0
        while i < current_step:
            try:
                files = []
                for filename in waste_files:
                    if f'waste{i}' in filename:
                        files.append(filename)
                final_files.append(files[-1])
                i += 1
                
            except IndexError:
                break    
        
    final_files.append(fuel_files[-1])
    
    dens = 0
    total_mats = {}
    for file in final_files:
        contents = read_bumat_file(file)
        dens += contents[3]
        mats = contents[6]
        for key in mats:
            try:
                total_mats[key] += mats.get(key)
            except:
                total_mats = {**total_mats, key : mats.get(key)}
    
    
    return total_mats


def total_inventory_list(x):
    mats_list = total_inventory(x[0])
    for key in mats_list:
        mats_list[key] = [mats_list.get(key)]
    for i in x[1:]:
        inv = total_inventory(i)
        for key in mats_list:
            mats_list[key].append(inv.get(key))
        
    return mats_list
#recycle()
#total_inventory(6)
#test = total_inventory_list(range(10))
#test = read_bumat_files(dirname = 'C:/Users/matti/Dropbox/Projekt_tillämpad/Code/Exempelkörning/SFR_TRU results/SFR_TRU')
#depsteps = depsteps('input.inp')

#vals = read_res_file('input0.inp_res.m')

"""    
# Testing functions
read_first_bumat()
TRU_mult = recycle(TRU_enr = 0.3, recycle_limit=[94000, 95000])
#print(waste[1003])#data = recycle(TRU_enr = 0.3)#, U_enr = 0.2

print(TRU_mult)

#sum of materials
sum_of_mats = 0
for mat in mats:
    sum_of_mats += mats.get(mat)
    print(mat)
print(sum_of_mats)


BU, days, mats = read_bumat_files()


# Variable to save
important_vars = ['ANA_KEFF', 
                  'BURNUP',
                  'BETA_EFF']

filename = 'Test/TestInput.inp_res.m'

read_bumat_file(filename)

vals = read_res_file(filename, important_vars)

plt.figure()
plt.plot(vals['BURNUP'][:,0], vals['ANA_KEFF'][:,0], '*')
plt.savefig('testplot')


print('read_bumat_files:')
burnup, days, materials = read_latest_bumat('Test')
# burnup, days, materials = read_bumat_files('Test')

"""
#test = read_bumat_files('.')