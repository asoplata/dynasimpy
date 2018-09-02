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

# The Specification object is where we describe the scientific model we want to use:
spec = dspy.Specification()
# LIMITATION: Things you can't name your populations (aka reserved words): 'pre', 'post', 'N', 'dt'
# LIMITATION: Things you can't parametrize right now: v, vars beginning with 'N_', vars ending in '_post'
spec.create_population(name='E',
                       size=20,
                       master_equations=master_equations,
                       mechanisms=['iNa', 'iK', 'iT', 'CaBuffer'])

spec.create_population(name='I',
                       size=10,
                       master_equations=master_equations,
                       mechanisms=['iNa', 'iK'])

spec.create_connection(direction='I->E', mechanisms=['iGABAa'])
spec.create_connection(direction='E->I', mechanisms=['iAMPA'])
spec.create_connection(direction='I->I', mechanisms=['iGABAa'])

# The Metadata object is where we specify everything EXCEPT the scientific model we want to use
md = dspy.Metadata()
# Metadata owns a dictionary called "simulator_options" where we put all our flags, including things like what kind
# of solver do we want to use, where do we want our data to go, etc.:
md.simulator_options = {
    'output_directory': 'testing'
}

# Metadata owns a list called "variations" where we put all the parameters we want to use instead of the default
# values in the mechanism files; this includes ranges of values if we want to use parameter sweeping.
# To simulate a single value of a parameter, in the "variations" list, include an element using the following syntax:
#     [ <population or direction name>,
#       <mechanism name or 'master_equations' if the parameter is only available there>,
#       <parameter name>,
#       <Brian 2 units to use>,
#       <value to use>]
# Example code:
#     # This would simulate only 1 simulation
#     md.variations = [
#         ['E', 'iNa', 'g_Na', 'msiemens', 50]
#     ]
# To sweep over the "Cartesian product" of multiple parameters, i.e. where you want to simulate over EVERY combination
# of values for all parameters, instead of "<value to use>", use a LIST of the values you want by wrapping your
# values in brackets.
# Example code:
#     # Below would simulate 3 simulations
#     md.variations = [
#         ['E', 'iNa', 'g_Na', 'msiemens', [30, 50, 70]]
#     ]
#     # Below would simulate 9, or 3x3, simulations
#     md.variations = [
#         ['E', 'iNa', 'g_Na', 'msiemens', [30, 50, 70]],
#         ['I', 'iNa', 'g_Na', 'msiemens', [20, 40, 60]]
#     ]
# To sweep over the "dot product" of multiple parameters, i.e. where you want to simulate over only each parameter
# value once and "match them together, instead of "<value to use>", use a TUPLE of the values you want by wrapping
# your values in parentheses.
# Example code:
#     # Below would simulate ONLY 3 simulations
#     md.variations = [
#         ['E', 'iNa', 'g_Na', 'msiemens', (30, 50, 70)],
#         ['I', 'iNa', 'g_Na', 'msiemens', (20, 40, 60)]
#     ]
# You can combine these rules for more customization of your sweeps.
# Example code:
#     # Below would simulate 27 simulations, or 3x3x3, since for every element in the tuples, every combination of
#     # elements in the lists would be simulated.
#     md.variations = [
#         ['E', 'iNa', 'g_Na', 'msiemens', [30, 50, 70]], # \_ 9 simulations \
#         ['I', 'iNa', 'g_Na', 'msiemens', [20, 40, 60]], # /                 \_ 9 x 3 simulations total
#         ['E', 'iK', 'g_K',   'msiemens', (10, 12, 14)], # \_ 3 simulations  /
#         ['I', 'iK', 'g_K',   'msiemens', ( 8, 10, 12)]  # /                /

md.variations = [
    ['E', 'master_equations', 'I_app', 'uA', [0,1,2]],
    ['E', 'PoissonInput','lambda','Hz',20]
]

# parameters = [['master_equations', 'I_app', 'uA', 5],
#               ['iNa', 'g_Na', 'msiemens', 120],
#               ['iK', 'g_K', 'msiemens', 77]])
# parameters = [['master_equations', 'I_app', 'uA', 0],
# ['iNa', 'g_Na', 'msiemens', 120],
# ['iK', 'g_K', 'msiemens', 36]])
# spec.connections[1]['parameters'] = {'tau_GABAa': '10*ms', 'g_GABAa': '0.1*msiemens'}
# spec.connections[2]['parameters'] = {'tau_d_AMPA': '2*ms', 'g_AMPA': '0.1*msiemens'}
# spec.connections[3]['parameters'] = {'tau_GABAa': '10*ms', 'g_GABAa': '0.1*msiemens'}


# Now let's simulate!!!
data = dspy.simulate(spec, md)

# data = dspy.simulate(spec, solver='rk4', random_flag="LULZ",
#                      vary=vary, save_data_flag=True, spike_detection_threshold=0*mV,
#                      spike_detection_refractory=1*ms)
# spike_detection_refractory=1*ms)

print('done-zo oh geez')
