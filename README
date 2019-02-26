### Script to submit MESA jobs to condor queue

Usage

1. [config.py] open config.py and specify the path to your mesa executable. Warning! Any 'inlist' file inside the same dir will be overwritten 

2. [config.py] specify the output directory

3. [config.py] specify the parameters you wish to explore (up to 3). For overshooting and metallicity, one only needs to specify "overshoot" and "initial_z" respectively. All related parameters (overshoot_f_above_*,initial_y,Zbase, etc.) will be modified automatically. See config.py.example   

4. Modify the base inlist file: templates/inlist.template
   Here you need to edit the lines that correspond to the parameters you specified above. For instance if one of your variables is 'initial_mass' then you need to change the regular mesa line 
   	> initial_mass = 1.0  
   to
	> initial_mass

   if one of your variables is initial_z then you also need to modify Zbase, initial_y and initial_he4
   No need to change the overshooting parameters
   Remember: You can only explore 3 variables at a time

5. Edit templates/condor.job.template and specify the desired number of CPU cores per job

6. Run the script 
   > python submit_jobs.py 
