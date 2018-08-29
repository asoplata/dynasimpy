#! /usr/bin/env python

# Pycharm notes:
# - Ctrl+8 adds a breakpoint

import dynasimpy as dspy

# LIMITATION: If you're using mechanism files, you MUST have the "current" variable in your voltage term of the
# "master_equations" variable.
master_equations = '''
dv/dt=(current + I_app)/Cm : volt
Cm = 1*uF : farad
I_app = 0*uA : amp
'''

# The Specification object is where we describe the model we want to use:
spec = dspy.Specification()
# LIMITATION: Things you can't name your populations (aka reserved words): 'pre', 'post', 'N', 'dt'
# LIMITATION: Things you can't parametrize right now: v, vars beginning with 'N_', vars ending in '_post'
spec.create_population(name = 'E',
                       size = 20,
                       master_equations = master_equations,
                       mechanisms= ['iNa', 'iK', 'iT', 'CaBuffer'],
                       parameters = [['master_equations', 'I_app', 'uA', 5],
                                     ['iNa', 'g_Na', 'msiemens', 120],
                                     ['iK', 'g_K', 'msiemens', 77]])

spec.create_population(name = 'I',
                       size = 10,
                       master_equations = master_equations,
                       mechanisms= ['iNa', 'iK'],
                       parameters = [['master_equations', 'I_app', 'uA', 0],
                                     ['iNa', 'g_Na', 'msiemens', 120],
                                     ['iK', 'g_K', 'msiemens', 36]])

spec.create_connection(index=1)
spec.connections[1]['direction'] = 'I->E'
spec.connections[1]['mechanism_list'] = 'iGABAa'
spec.connections[1]['parameters'] = {'tau_GABAa': '10*ms', 'g_GABAa': '0.1*msiemens'}

spec.create_connection(index=2)
spec.connections[2]['direction'] = 'E->I'
spec.connections[2]['mechanism_list'] = 'iAMPA'
spec.connections[2]['parameters'] = {'tau_d_AMPA': '2*ms', 'g_AMPA': '0.1*msiemens'}

spec.create_connection(index=3)
spec.connections[3]['direction'] = 'I->I'
spec.connections[3]['mechanism_list'] = 'iGABAa'
spec.connections[3]['parameters'] = {'tau_GABAa': '10*ms', 'g_GABAa': '0.1*msiemens'}



# Entries need to be "immutable", e.g. of tuple type
vary = {
    'E': {'Iapp': tuple([0, 10, 20])*uA},
    'I->E': {'tauD': tuple([5, 15, 25])*ms}
}

data = dspy.simulate(spec)
# data = dspy.simulate(spec, solver='rk4', random_flag="LULZ",
#                      vary=vary, save_data_flag=True, spike_detection_threshold=0*mV,
#                      spike_detection_refractory=1*ms)
# spike_detection_refractory=1*ms)

print('done-zo oh geez')
