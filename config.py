#path to folder that contains the mesa executable
mesa_root_dir = '/vol/aibn185/data1/jantoniadis/mesa-r10398'
mesa_directory = '/vol/aibn185/data1/jantoniadis/mesa-r10398/star/test_suite/Condor'
out_directory= '/vol/aibn185/data1/jantoniadis/HeCoresCondor/full_grid'


#Can explore up to three variables

variable1 = {'name': 'initial_mass',
             'location': 'inlist_var',
             'type': 'array',
             'minimum': 1.5,
             'maximum': 3.0,
             'step': 0.1,
}

variable2 = {'name': 'initial_z',
             'location': 'inlist_var',
             'type': 'predetermined_array',
             'values': [0.00001,0.0014]
}

variable3 = {'name': 'overshoot',
             'location': 'inlist_var',
             'type': 'predetermined_array',
             'values': [0.000,0.014,0.016]
}
