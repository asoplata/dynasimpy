from .Model import Model
from .SimulatorOptions import SimulatorOptions

# In general, the below is not recommended, but it is specifically recommended by the Brian2 package.
from brian2 import *

# import ipdb

import json
# import jsonpickle
# import pickle

def simulate(spec, **kwargs):
    """This is the master function, so to speak"""

    # TODO: if first arg is string, search mechanism/model path for a "model file". If it's a Specification object, then the user wants to create a new spec
    # TODO: this implies that user needs to be able to load a model file and then change the...what? spec?

    # in python, passed ints and strs are immutable??? TODO test
    # 0.1 Validate the specification
    spec = spec.validate_spec()

    # 0.2 process non-specification arguments
    if bool(kwargs):
        # debug
        print('--> kwargs before vary pop is {}'.format(kwargs))

        # 0.2.1 Remove vary from the options
        if 'vary' in kwargs:
            vary = kwargs.pop('vary')

        # debug
        print('--> vary is {}'.format(vary))
        for key, value in kwargs.items():
            print(key, ":", value)

        # 0.2.2 Validate the simulator options
        sim_ops = SimulatorOptions()

        # debug
        print('simops before validation {}'.format(sim_ops.__dict__))

        sim_ops.validate_options(options=kwargs)
        # debug
        print('simops after validation {}'.format(sim_ops.__dict__))
    else:
        sim_ops = SimulatorOptions()
        print('simops WITHOUT validation {}'.format(sim_ops.__dict__))

    # 0.3 Convert DynaSim specification to Brian2-compatible model
    brian_model = Model(spec, sim_ops)
    # print(brian_model)

    # brian_model_enc = jsonpickle.encode(brian_model)

    # with open('full_brian_model.json','w') as outfile:
    #     json.dump(brian_model_enc, outfile)

    # with open('full_brian_model.pickle','w') as outfile:
    #     pickle.dump(brian_model, outfile)

    # ipdb.set_trace()

    # pass
    # for some reason, `Network(collect())` not finding objects embedded in the brian_model struct, but can add them artificially
    net = Network()


    ## Create monitors to save data
    neuron1_data = StateMonitor(brian_model.neurons[1]['neuron_object'], 'v', record=True)
    # spikes = SpikeMonitor(brian_model.neurons[1]['neuron_object'])

    ## Gather all the model components, including neurons, synapses, and monitors
    net.add(brian_model.neurons[1]['neuron_object'])
    net.add(neuron1_data)

    # Initial conditions
    brian_model.neurons[1]['neuron_object'].v = -65*mV
    brian_model.neurons[1]['neuron_object'].m_Na = 0.1
    brian_model.neurons[1]['neuron_object'].h_Na = 0.04
    brian_model.neurons[1]['neuron_object'].n_K =  0.0
    # very sensitive
    brian_model.neurons[1]['neuron_object'].h_T =  0.0
    brian_model.neurons[1]['neuron_object'].CaBuffer =  0.0001

    prefs.codegen.target = 'numpy'

    # # debug
    # ipdb.set_trace()
    # suddenly, need to now manually add objects via Network.add(<object>?), not that that's not clear
    # TODO need to fix network collection
    # print('derp3')
    # running `run` by itself just uses `Network(collect())`, which isn't working for us right now
    net.run(100*ms, report='text')

    figure()
    plot(neuron1_data.t/ms, neuron1_data[0].v/mV)

    # # print('derp3')
    # run(100*ms, report='text')
    pass

    # section: convertSpecToBrianModel (single object?)
    # section: for # of entries in spec parameters in each population and connection, apply individual parameter modifications from runfile
    #     oh yeah, wait until Brian models built to apply mods http://brian2.readthedocs.io/en/stable/advanced/namespaces.html
    #     `<nrgroup>.namespace['<name>'] = new_value` is basically exact same thing as applymods, only that namespace can't be read from and only final value is used
    # section: if vary present, use dsVary2Modifications

    # later section: make sure collect() works on brian objects as subobjects

