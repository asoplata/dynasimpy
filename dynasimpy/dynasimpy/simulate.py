from . import Metadata
from . import BrianModel
from . import Specification

# In general, the below is not recommended, but it is specifically recommended by the Brian2 package.
from brian2 import *
import ujson as json


def simulate(spec: Specification, md: Metadata):
    """
    This is the master function to run simulation(s).

    Depending on the options specified, this performs a simulation locally,
    prepares simulation(s) for the user to run either in console or in a newly-opened Jupyter notebook, or submits
    a batch of simulation(s) to run on a cluster. This is NOT a "pure" function (i.e., it has state changes/"side
    effects"), but, with few exceptions, should only be calling pure functions. In general, only this function and
    those that call it should have state changes/side effects, not functions lower on the chain.

    :param spec: The Specification object which describes the scientific model to use in simulation(s)
    :type spec: Specification
    :param md: The Metadata object which describes how to run any simulation(s) of the model, including parameter
    variations to sweep over, flags, etc.
    :type md: Metadata
    :return:
    """

    # If no internal flags detected, then add them
    if md.simulator_options.get('preprocessed_flag') is None:
        md.simulator_options.update({
            'jupyter_flag': True,
            'preprocessed_flag': False,
            'simulation_number': 0,
            'standalone_flag': False
        })

    md.validate()

    # 1.0 This is the "setup" block; see 2.0 below for the "run" block
    if md.simulator_options['preprocessed_flag'] is False:
        # 1.1 Create the output location
        md.simulator_options['output_directory'] = md.create_output_location()

        bm = BrianModel(spec)
        bm.load_mechanisms()
        bm.validate_mechanisms()
        bm.parse_connections_directions()
        bm.setup_population_mechanisms()
        # bm.setup_connection_mechanisms()

        # 1.2 Load and validate the connection mechanisms
        # 1.3 Load and validate the population mechanisms
        pass

    # 0.3 Convert DynaSim specification to Brian2-compatible model
    brian_model = BrianModel(spec, md)
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

