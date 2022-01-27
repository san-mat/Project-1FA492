############################################################
#     	        Serpent interaction script                 #

#            	auth Kristoffer Franzen                    #
#            	     Mattias Sandnabba                     #
############################################################

import os
import signal
import math
import time
import numpy as np
from Code import * 


# Open original input for reading

file_in = open('./input.inp','r')

# Open a new input file for writing

file_out = open('./input0.inp','w')

# Write input files based on original file

for line in file_in:
    file_out.write(line)

file_in.close()
file_in = open('./input.inp','r')

final_out = open('final.inp', 'w')
waste_out = open('waste.inp', 'w')
skip = False
for line in file_in:
	if line.startswith('dep '):
		skip = True
	elif not skip:
		waste_out.write(line*(not 'set powdens' in line and not 'fuel.txt' in line))
		waste_out.write('include FR_SNF.txt'*('fuel.txt' in line))
		final_out.write(line*(not 'set powdens' in line and not 'fuel.txt' in line))
		final_out.write('include total_inventory.txt'*('fuel.txt' in line))
	elif skip and line.strip() and not line.strip().startswith('%'):
		try:
			float(line.split('%')[0])
		except ValueError:
			skip = line.startswith('dep ')
			waste_out.write(line*(not skip and not 'set powdens' in line))
			final_out.write(line*(not skip and not 'set powdens' in line))
final_out.write('set powdens 0\ndep decstep\n')
waste_out.write('set powdens 0\n')
for x in [1 ,3 ,10, 30, 100, 300, 1000, 3000, 1e4, 3e4, 1e5, 3e5, 1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9]:
	final_out.write(f'{x}\n')
		
# Close files
file_in.close()
file_out.close()
waste_out.close()
final_out.close()



# How many recycles? 

limit = range(94000,99999)
TRU = 0.15
U235 = None
totalcycles = 10
depsteps = depsteps()

N_external_U235 = []
N_external_TRU = []
waste = []
fuel = []
os.system('rm *.bumat*')
data = recycle(filename = 'SNF_LWR.txt', TRU_enr = TRU, U_enr = U235,recycle_isotopes = limit)
N_external_TRU.append(data[0])
N_external_U235.append(data[1])
waste.append(data[2])
fuel.append(data[3])

for x in range(0, totalcycles):

    # Open original input for reading
	lastCycleTime = time.time()
	file_in = open('./input.inp','r')
	step = 0
	# Open a new input file for writing

	file_out = open(f'./input{x}.inp','w')

	# Write original input to new file

	for line in file_in:
		file_out.write(line)

	file_out.close()


	# Run simulation
	print('sss2 -omp 32 -noplot ./input{x}.inp &')
	# Execute the command string
 
	os.system(runcommand)
	time.sleep(30)

		
	# Wait for last expected bumat file


	while not f'input{x}.inp.bumat{depsteps - 1}' in os.listdir():
		# Sleep for two seconds
		time.sleep(2)
			
	time.sleep(5)


	data = recycle(TRU_enr = TRU, U_enr = U235,recycle_isotopes = limit)
	N_external_TRU.append(data[0])
	N_external_U235.append(data[1])
	waste.append(data[2])
	fuel.append(data[3])
	

	if x < totalcycles: #  Decay of waste simulation
		file_in = open('./waste.inp','r')

		# Open a new input file for writing

		file_out = open(f'./waste{x}.inp','w')

		# Write original input to new file
		cyclelength = read_latest_bumat()[1]
		for line in file_in:
			file_out.writelines(line)
		file_out.writelines('dep decstep\n')
		for i in range(totalcycles-x):
			file_out.write(f'{float(cyclelength)}\n')
		file_out.close()

		os.system(f'sss2 -omp 64 -noplot ./waste{x}.inp &')
"""
		while not f'waste{x}.inp.bumat{totalcycles-x}' in os.listdir():
			time.sleep(2)
"""	

# Save recycle() outputs and start final 
np.save('inventory.npy', np.array(total_inventory()))	
np.save('N_external_TRU.npy', np.array(N_external_TRU))
np.save('N_external_U235.npy', np.array(N_external_U235))
np.save('waste.npy', np.array(waste))
np.save('fuel.npy', np.array(fuel))

os.system(f'sss2 -omp 64 ./final.inp')


