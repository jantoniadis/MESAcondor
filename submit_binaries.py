from __future__ import print_function 
import numpy as np
import os

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove


from config_binary import * 





overshoot_f_variables = ['overshoot_f_above_nonburn_core = ',
                       'overshoot_f_above_nonburn_shell = ',
                       'overshoot_f_below_nonburn_shell = ',
                       'overshoot_f_above_burn_h_core = ',
                       'overshoot_f_above_burn_h_shell = ',
                       'overshoot_f_below_burn_h_shell = ',
                       'overshoot_f_above_burn_he_core = ',
                       'overshoot_f_above_burn_he_shell = ',
                       'overshoot_f_below_burn_he_shell = ',
                       'overshoot_f_above_burn_z_core = ',
                       'overshoot_f_above_burn_z_shell = ',
                       'overshoot_f_below_burn_z_shell = ']

overshoot_f0_variables = [ 'overshoot_f0_above_nonburn_core = ',
                           'overshoot_f0_above_nonburn_shell = ',
                           'overshoot_f0_below_nonburn_shell = ',
                           'overshoot_f0_above_burn_h_core = ',
                           'overshoot_f0_above_burn_h_shell = ',
                           'overshoot_f0_below_burn_h_shell = ',
                           'overshoot_f0_above_burn_he_core = ',
                           'overshoot_f0_above_burn_he_shell = ',
                           'overshoot_f0_below_burn_he_shell = ',
                           'overshoot_f0_above_burn_z_core = ',
                           'overshoot_f0_above_burn_z_shell = ',
                           'overshoot_f0_below_burn_z_shell = ']







def replace_line(file_path, old_line, new_line, new_file_path):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(old_line, new_line))
    move(abs_path, new_file_path)



def modify_inlist_value(inlist,variable_name,value,inlist_out):

    if variable_name == 'overshoot':
        if value > 0:
            for f in overshoot_f_variables:
                replace_line(inlist,f+'0.000',f+np.str(value),inlist_out)
            for f in overshoot_f0_variables:
                replace_line(inlist,f+'0.000',f+'0.004',inlist_out)
    elif variable_name == 'initial_z':
        replace_line(inlist,'initial_z','initial_z = '+np.str(value),inlist_out)
        y = 1 - value 
        replace_line(inlist,'initial_y','initial_y = '+np.str(y),inlist_out)
        replace_line(inlist,'initial_he4','initial_he4 = '+np.str(y),inlist_out)
        replace_line(inlist,'Zbase','Zbase = '+np.str(value),inlist_out)
    else:
        replace_line(inlist,variable_name,variable_name + ' = ' + np.str(value),inlist_out)
        
        
        



for variable in grid_variables:
    if variable['type'] == 'array':
        variable['values'] = np.arange(variable['minimum'],
                                      variable['maximum']+variable['step'],
                                      variable['step'])


def main():
    for value1 in variable1['values']:
        for value2 in variable2['values']:
            for value3 in variable3['values']:
              output_directory = "bin{:0.4f}_{:0.4f}_{:0.4f}".format(value1,value2,value3)



              output_directory = os.path.join(out_directory,output_directory)
              condor_job = os.path.join(output_directory,'condor.job')
              run_mesa = os.path.join(output_directory,'run_mesa.sh')
              inlist1 = os.path.join(output_directory,'inlist1')
              inlist2 = os.path.join(output_directory,'inlist2')
              inlist_project = os.path.join(output_directory,'inlist_project')
              model_name = os.path.join(output_directory,'final_model.mod')
              final_profile_name = os.path.join(output_directory,'final_profile.data')
            
              if not os.path.exists(output_directory):
                os.makedirs(output_directory)
                os.system('cp '+'templates/inlist1.template '+inlist1)
                #os.system('cp '+'templates/inlist2.template '+inlist2)
                os.system('cp '+'templates/inlist_project.template '+inlist_project)
                
                
                inlist_var1 = os.path.join(output_directory,variable1['inlist'])
                inlist_var2 = os.path.join(output_directory,variable2['inlist'])
                inlist_var3 = os.path.join(output_directory,variable3['inlist'])
                
                modify_inlist_value(inlist_var1,variable1['name'],value1,inlist_var1)
                modify_inlist_value(inlist_var2,variable2['name'],value2,inlist_var2)
                modify_inlist_value(inlist_var3,variable3['name'],value3,inlist_var3)

                replace_line('templates/condor.job.template',
                             'Log =', 
                             'Log =' + os.path.join(output_directory,'condor.log'),
                             condor_job)
                replace_line(condor_job,
                             'Output =', 
                             'Output =' + os.path.join(output_directory,'condor.out'),
                             condor_job)
                #replace_line(condor_job,
                #             'Executable = run_mesa.sh', 
                #             'Executable ='+os.path.join(output_directory,'run_mesa.sh'),
                #             condor_job)
                replace_line(condor_job,
                             'environment = OMP_NUM_THREADS=1;PYTHONBUFFERED=1',
                             'environment = OMP_NUM_THREADS=1;PYTHONBUFFERED=1;MESA_DIR=' +mesa_root_dir,
                             condor_job)
                replace_line(condor_job,
                             'Error =', 
                             'Error =' + os.path.join(output_directory,'condor.err'),
                             condor_job)
                replace_line('templates/run_mesa.sh.template',
                             'cp -r', 
                             'cp -r ' + os.path.join(mesa_directory,'*')+ ' '+output_directory,
                             run_mesa)
                replace_line(run_mesa,
                             './rn', 
                             os.path.join(output_directory,'*') + 'binary',
                             run_mesa)
                os.system('chmod +x ' + run_mesa)
                print('')
                print('creating files in' + output_directory)
                print('')
                os.chdir(output_directory)
                os.system('condor_submit condor.job')
                os.chdir(script_directory) 


if __name__ == "__main__":
    main()


    

