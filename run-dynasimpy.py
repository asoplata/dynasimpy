#!/bin/env/python

# TODO: for units
from brian2 import *
import dynasimpy as dspy

# should have "current" in the master equation
master_eqns = '''
dv/dt=(current + I_app)/Cm : volt
Cm = 1*uF : farad
I_app = 0*uA : amp
'''

# The parentheses are important!
spec = dspy.Specification()
spec.create_population(index=1)
# things you can't (or shouldn't) name your populations (aka reserved words): 'pre', 'post', 'N', 'dt'
spec.populations['1']['name'] = 'E'
spec.populations['1']['size'] = 10
spec.populations['1']['master_eqns'] = master_eqns
# spec.populations['1']['mechanism_list'] = ['iNa', 'iK']
spec.populations['1']['mechanism_list'] = ['iNa', 'iK', 'iT', 'CaBuffer']
# - things you can't parametrize right now: v, vars beginning with 'N_', vars ending in '_post'
# - setting parameters to have celltype-wide unique names (pre-runtime) is not needed for the programming, but instead
# needed for the parametrization here.
# - Similarly, SVs as well, esp in synapses, should be unique as well, not for the programming, but instead for setting
# initial conditions!
# - just be clear: people CAN use g, E, I, etc. without suffices in mechanism files, but then they could only parametrize
# files by specifying the
# - there are 2 options here:
#     1. keep it like it is, leave it to the mechanism files to add mechanism-specific subscripts to the variables and state variables
#     2. trivially, change Model.convert_mechanism to add the mechanism name as a subscript to the vars

# wow, giving these as values which get turned into strings causes the simulation run command to actually fail sili
spec.populations['1']['parameters'] = {'I_app': '5*uA', 'g_Na': '120*msiemens', 'g_K': '77*msiemens'}

spec.create_population(index=2)
spec.populations['2']['name'] = 'I'
spec.populations['2']['size'] = 20
spec.populations['2']['master_eqns'] = master_eqns
spec.populations['2']['mechanism_list'] = ['iNa', 'iK']
spec.populations['2']['parameters'] = {'Iapp': '0*uA', 'g_Na': '120*msiemens', 'g_K': '36*msiemens'}

spec.create_connection(index=1)
spec.connections['1']['direction'] = 'I->E'
spec.connections['1']['mechanism_list'] = 'iGABAa'
spec.connections['1']['parameters'] = {'tau_GABAa': '10*ms', 'g_GABAa': '0.1*msiemens'}

spec.create_connection(index=2)
spec.connections['2']['direction'] = 'E->I'
spec.connections['2']['mechanism_list'] = 'iAMPA'
spec.connections['2']['parameters'] = {'tau_d_AMPA': '2*ms', 'g_AMPA': '0.1*msiemens'}

spec.create_connection(index=3)
spec.connections['3']['direction'] = 'I->I'
spec.connections['3']['mechanism_list'] = 'iGABAa'
spec.connections['3']['parameters'] = {'tau_GABAa': '10*ms', 'g_GABAa': '0.1*msiemens'}

# Entries need to be "immutable", e.g. of tuple type
vary = {
    'E': {'Iapp': tuple([0, 10, 20])*uA},
    'I->E': {'tauD': tuple([5, 15, 25])*ms}
}

# data = dspy.simulate(spec)
data = dspy.simulate(spec, solver='rk4', random_flag="LULZ",
                     vary=vary, save_data_flag=True, spike_detection_threshold=0*mV,
                     spike_detection_refractory=1*ms)

print('done-zo oh geez')
