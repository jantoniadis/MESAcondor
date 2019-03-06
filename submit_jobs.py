from __future__ import print_function 
import numpy as np
import os

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove


from config import * 





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



grid_variables = [variable1,variable2,variable3]



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
                output_directory = "{:0.4f}_{:0.4f}_{:0.4f}".format(value1,value2,value3)



                output_directory = os.path.join(out_directory,output_directory)
                LOGS = os.path.join(output_directory,'LOGS')
                photos = os.path.join(output_directory,'photos')
                model_name = os.path.join(output_directory,'final_model.mod')
                final_profile_name = os.path.join(output_directory,'final_profile.data')
            
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)

                replace_line('templates/inlist.template', 
                             'save_model_filename', 
                             'save_model_filename = ' + '\''+model_name+'\'', 
                             'inlist')

                replace_line('inlist', 
                             'filename_for_profile_when_terminate', 
                             'filename_for_profile_when_terminate =' +  '\''+final_profile_name+ '\'', 
                             'inlist')

                replace_line('inlist', 
                             'log_directory', 
                             'log_directory = ' +  '\''+LOGS+'\'', 
                             'inlist')

                replace_line('inlist', 
                             'photo_directory', 
                             'photo_directory = ' +  '\''+photos+'\'', 
                             'inlist')

                modify_inlist_value('inlist',variable1['name'],value1,'inlist')
                modify_inlist_value('inlist',variable2['name'],value2,'inlist')
                modify_inlist_value('inlist',variable3['name'],value3,'inlist')

                replace_line('templates/condor.job.template',
                             'Log =', 
                             'Log =' + os.path.join(output_directory,'condor.log'),
                             'condor.job')
                replace_line('condor.job',
                             'Output =', 
                             'Output =' + os.path.join(output_directory,'condor.out'),
                             'condor.job')
                replace_line('condor.job',
                             'environment = OMP_NUM_THREADS=1;PYTHONBUFFERED=1',
                             'environment = OMP_NUM_THREADS=1;PYTHONBUFFERED=1;MESA_DIR=' +mesa_root_dir,
                             'condor.job')
                replace_line('condor.job',
                             'Error =', 
                             'Error =' + os.path.join(output_directory,'condor.err'),
                             'condor.job')
                replace_line('templates/run_mesa.sh.template',
                             'cd', 
                             'cd ' + mesa_directory,
                             'run_mesa.sh')
                os.system('cp inlist ' + output_directory)
                os.system('cp inlist ' + mesa_directory)
                os.system('chmod +x run_mesa.sh')
                os.system('condor_submit condor.job')
                #clean up
                #os.system('rm -f inlist')
                #os.system('rm condor.job')
                #os.system('rm run_mesa.sh')


if __name__ == "__main__":
    main()


    

