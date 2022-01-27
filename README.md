# Project-1FA492
---
**Run simulation**

A new simulation is set up by creating a new directory and placing
- *Code.py*
- *serpent_iter.py*
- *SNF_LWR.txt* or any Serpent compatible fuel card containing TRU elements and uranium
- *input.inp* or any Serpent input file that produces .bumat files

into the empty directory. The fuel is then recycled according to the parameters specified in serpent_iter.py.

-----------------------------------
**Recycling**

Important input parameters to *recycle*

- TRU_enr: sets fraction of TRU in fuel
- U235_enr: sets fraction of U235 in fuel
- recycle_isotopes: sets what range of isotopes (ZZAAA) that should be recycled.
- exclude_isotopes: Exclude recycling of list of isotopes inside the recycling range
- Temp: Overwrite temperature from *SNF_LWR*. can be '09c', '12c', '15c', '18c'

If left to default values, the code will only set density and remove fission products and uranium decay chain isotopes.

Output of the recycling code is saved in binary .npy files. They can be opened with numpy for analysis.

-----------------------------------
**Postprocessing**

Two post-processing scripts are included as examples. They produce the plots and results found in the report using the functions developed.

For the scripts to work, they should be placed outside the directories that should be analysed (directories containing simulation results). 
*Code.py* must be included in the same directory as the postprocessing script.
