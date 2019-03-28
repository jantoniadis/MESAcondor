#path to folder that contains the mesa executable
mesa_root_dir = '/vol/aibn1107/data2/schanlar/mesa-r10398'
mesa_directory = '/vol/aibn1107/data2/schanlar/mesa-r10398/binary/test_suite/Condor'
out_directory= '/vol/hal/halraid/schanlar/Condor/Binaries'
script_directory = '/vol/aibn1107/data2/schanlar/MESAcondor'

#path to folder that contains the HeZAMS models
init_dir = '/vol/hal/halraid/schanlar/Condor/HeZAMS/NO_OVERSHOOT/*'
#Can explore up to three variables




import numpy as np
import glob
import os
periods = 10**np.arange(-1.,3.6,0.1)

HeZAMS_paths = [path for path in glob.glob(init_dir)]
initial_model_name = []
initial_model_path = []
for i in HeZAMS_paths:
	os.chdir(i)
	temp = glob.glob('*.mod')
	try:
		initial_model_path.append(i+'/'+temp[0])
		temp[0] = temp[0].replace('.mod', '')
		initial_model_name.append(temp[0])
	except:
		continue

initial_model_name.sort()
initial_model_path.sort()	


variable1 = {'name': 'm1',
             'type': 'array',
             'minimum': 1.0,
             'maximum': 3.5,
             'step': 0.1,
             'inlist':'inlist_project'
}

variable2 = {'name': 'initial_period_in_days',
             'type': 'predetermined_array',
             'values': periods,
             'inlist':'inlist_project'
}

variable3 = {'name': 'saved_model_name',
             'type': 'predetermined_array',
             'values': (initial_model_name, initial_model_path),
             'inlist':'inlist1'
}

grid_variables = [variable1,variable2,variable3]

