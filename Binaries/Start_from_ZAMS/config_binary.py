#path to folder that contains the mesa executable
mesa_root_dir = '/vol/aibn185/data1/jantoniadis/mesa-r10398'
mesa_directory = '/vol/aibn185/data1/jantoniadis/mesa-r10398/binary/test_suite/Condor'
out_directory= '/vol/hal/halraid/jantoniadis/HeCores/Condor/tests'
script_directory = '/vol/aibn185/data1/jantoniadis/MESAcondor'

#Can explore up to three variables




import numpy as np
periods = 10**np.arange(-1.,3.6,0.1)



variable1 = {'name': 'm1',
             'type': 'array',
             'minimum': 1.5,
             'maximum': 3.5,
             'step': 0.1,
             'inlist':'inlist_project'
}

variable2 = {'name': 'initial_period_in_days',
             'type': 'predetermined_array',
             'values': periods,
             'inlist':'inlist_project'
}

variable3 = {'name': 'initial_z',
             'type': 'predetermined_array',
             'values': [0.02],
             'inlist':'inlist1'
}

grid_variables = [variable1,variable2,variable3]
