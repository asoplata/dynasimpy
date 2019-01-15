from . import Metadata
from . import Specification

# In general, the below is not recommended, but it is specifically recommended by the Brian2 package.
import brian2 as b2

import ujson as json

import copy
import os
import sys
# Apparently "ruamel.yaml" is currently the best-supported/most up-to-date Python YAML lib
from ruamel.yaml import YAML
yaml = YAML(typ='safe')


class BrianModel:
    def __init__(self, spec: Specification):
        self.connections = copy.deepcopy(spec.connections)
        self.populations = copy.deepcopy(spec.populations)

        for pop in self.populations:
            for mechanism in self.populations[pop]['mechanisms']:
                self.populations[pop][mechanism] = {}

        for cxn in self.connections:
            for mechanism in self.connections[cxn]['mechanisms']:
                self.connections[cxn][mechanism] = {}

        # Overall process:
        # 1.0 Load and convert connections from specification
        # 2.0 Load and convert populations from specification
        # 3.0 Build complete equations string for each neuron type
        # 4.0 Build complete equations string for each synapse type
        # 5.0 TODO NOPE Apply modifications from either parametrization or variation by creating namespace_parametrizations and _variations
        # 5.1 Apply single parametrization via namespacing
        # 5.2 TODO NOPE Apply varied parameters via namespacing
        # 6.0 Save everything needed for reproducing model simulation!
        # 6.1 Save model equations, structure, and namespacing
        # 6.2 Save simulator options
        # 7.0 Create neuron objects
        # 8.0 Create synapse objects

        # # 1.0 Load and convert connections from specification
        # for index, connection in spec.connections.items():
        #     for mechanism in spec.connections[index]['mechanism_list']:
        #         self.synapses[index][mechanism]['converted_eqns'] = self.convert_mechanism(raw_eqns=self.synapses[index][mechanism]['raw_eqns'],
        #                                                                                    mech=self.synapses[index][mechanism]['name'],
        #                                                                                    source=self.synapses[index]['source'],
        #                                                                                    target=self.synapses[index]['target'])
        #         # Only grab current if mechanism prefixed with 'i' like in DynaSim
        #         if mechanism.startswith('i'):
        #             self.synapses[index][mechanism]['current'] = {}
        #             # use .eq_names, NOT .names or anything else, so that current will only be identified, once, by its definition (e.g. if an equation uses a current from another mechanism)
        #             current_object = Equations(self.synapses[index][mechanism]['converted_eqns']['target_neuron_eqns'])
        #             self.synapses[index][mechanism]['current']['name'] = str([value for value in current_object.eq_names
        #                                                                       if value.startswith('I_')][0])
        #             # self.synapses[index][mechanism]['current']['name'] = str([value for value in
        #             #                                                           self.synapses[index][mechanism]['converted_eqns']['target_neuron_eqns'].eq_names
        #             #                                                           if value.startswith('I_')][0])
        #             pass
        #         # output['current']['equation'] = str([value for key, value in output['target_neuron'].items() if key.startswith('I_')][0])

        # # 2.0 Load and convert populations from specification
        # for index, population in spec.populations.items():
        #     # apparently referring to variables/arrays followed by an underscore will refer to the variable without units?
        #     # http://brian2.readthedocs.io/en/stable/introduction/changes.html?highlight=volts%20seconds
        #     self.neurons[index] = {}
        #     self.neurons[index]['name'] = spec.populations[index]['name']
        #     self.neurons[index]['size'] = spec.populations[index]['size']
        #     self.neurons[index]['master_equations'] = spec.populations[index]['master_equations']
        #     self.neurons[index]['mechanism_list'] = spec.populations[index]['mechanism_list']

            # for mechanism in spec.populations[index]['mechanism_list']:
            #     self.neurons[index][mechanism] = {}
            #     self.neurons[index][mechanism]['name'] = mechanism
            #     self.neurons[index][mechanism]['raw_eqns'] = self.lookup_mechanism(mechanism)
            #     self.neurons[index][mechanism]['converted_eqns'] = self.convert_mechanism(raw_eqns=self.neurons[index][mechanism]['raw_eqns'],
            #                                                                               mech=self.neurons[index][mechanism]['name'],
            #                                                                               neuron=self.neurons[index]['name'])
            #     if mechanism.startswith('i'):
            #         self.neurons[index][mechanism]['current'] = {}
            #         # use .eq_names, NOT .names or anything else, so that current will only be identified, once, by its definition (e.g. if an equation uses a current from another mechanism)
            #         current_object = Equations(self.neurons[index][mechanism]['converted_eqns']['neuron_eqns'])
            #         self.neurons[index][mechanism]['current']['name'] = str([value for value in current_object.eq_names
            #                                                                  if value.startswith('I_')][0])

        # # 3.0 Build complete equations string for each neuron type
        # for index, value in self.neurons.items():
        #     self.neurons[index]['full_neuron_eqns'] = ''
        #     self.neurons[index]['full_neuron_eqns'] += self.neurons[index]['master_equations'] + '\n'
        #     items_in_current = []

            # # add all contributions from intrinsic mechs
            # for mechanism in self.neurons[index]['mechanism_list']:
            #     self.neurons[index]['full_neuron_eqns'] += self.neurons[index][mechanism]['converted_eqns']['neuron_eqns'] + '\n'
            #     if mechanism.startswith('i'):
            #         items_in_current.append(self.neurons[index][mechanism]['current']['name'])

            # # add all contributions from synaptic mechs
            # for synapse, synapse_value in self.synapses.items():
            #     if self.synapses[synapse]['target'] == self.neurons[index]['name']:
            #         for mechanism in self.synapses[synapse]['mechanism_list']:
            #             self.neurons[index]['full_neuron_eqns'] += self.synapses[synapse][mechanism]['converted_eqns']['target_neuron_eqns'] + '\n'
            #             if mechanism.startswith('i'):
            #                 items_in_current.append(self.synapses[synapse][mechanism]['current']['name'])

            # # string magic, i love python
            # items_in_current[1:] = ['+' + string for string in items_in_current[1:]]
            # self.neurons[index]['full_neuron_eqns'] = self.neurons[index]['full_neuron_eqns'].replace('current', ''.join(items_in_current))

            # # TODO try catch Equations errors about being malformed
            # try:
            #     Equations(self.neurons[index]['full_neuron_eqns'])
            # except:
            #     print("Could not interpret neuron population {} as proper Equations:".format(index), sys.exc_info()[0])
            #     raise

        # # 4.0 Build complete equations string for each synapse type
        # for index, value in self.synapses.items():
        #     for mechanism in self.synapses[index]['mechanism_list']:
        #         self.synapses[index][mechanism]['full_synapse_eqns'] = self.synapses[index][mechanism]['converted_eqns']['synapse_eqns'] + '\n'
        #         try:
        #             Equations(self.synapses[index][mechanism]['full_synapse_eqns'])
        #         except:
        #             print("Could not interpret synapse connection {}, mechanism {} as proper Equations:".format(index, mechanism), sys.exc_info()[0])
        #             raise

        # # 5.0 Apply modifications from either parametrization or variation by creating namespace_parametrizations and _variations
        # # reasons for applying modifications after the initial string interpretation from the spec:
        # #   - can keep namespacing changes separate from initial model, built entirely on mech files/raw
        # #   - can make explicit what's being varied!
        # #   - can easily make full throwaway Equations easily to check for names
        # # 5.1 Apply single parametrization via namespacing
        # for index, value in spec.populations.items():
        #     self.neurons[index]['namespace_parametrizations'] = {}

            # identifier_string_addition = '_' + self.neurons[index]['name']
            # test_master_equations_object = Equations(self.neurons[index]['master_equations'])
            # test_neuron_eqns_object = Equations(self.neurons[index]['full_neuron_eqns'])

            # for parameter, parameter_value in spec.populations[index]['parameters'].items():
            #     # apply parameters to master_equations
            #     for name in test_master_equations_object.names:
            #         if name.startswith(parameter):
            #             if (   parameter == 'v'
            #                 or parameter.startswith('N_')
            #                 or parameter.endswith('_total')
            #                 or parameter.endswith('_total_post')):
            #                 sys.exit("The parameter '{}' of neuron index {} is not valid.".format(parameter, index))
            #             self.neurons[index]['namespace_parametrizations'][parameter + identifier_string_addition] = str(parameter_value)

                # for name in test_neuron_eqns_object.names:
                #     if name.startswith(parameter):
                #         if (   parameter == 'v'
                #             or parameter.startswith('N_')
                #             or parameter.endswith('_total')
                #             or parameter.endswith('_total_post')):
                #             sys.exit("The parameter '{}' of neuron index {} is not valid.".format(parameter, index))

                        # self.neurons[index]['namespace_parametrizations'][parameter + identifier_string_addition] = str(parameter_value)

        # for index, value in spec.connections.items():
        #     for mechanism in self.synapses[index]['mechanism_list']:
        #         self.synapses[index][mechanism]['namespace_parametrizations'] = {}

                # identifier_string_addition = ''
                # # identifier_string_addition = '_' + self.synapses[index]['source'] + '_' + self.synapses[index]['target']
                # test_synapse_eqns_object = Equations(self.synapses[index][mechanism]['full_synapse_eqns'])

                # for parameter, parameter_value in spec.connections[index]['parameters'].items():
                #     # apply parameters to master_equations
                #     for name in test_synapse_eqns_object.names:
                #         if name.startswith(parameter):
                #             if (   parameter == 'v'
                #                 or parameter.startswith('N_')
                #                 or parameter.endswith('_total')
                #                 or parameter.endswith('_total_post')):
                #                 sys.exit("The parameter '{}' of synapse index {} is not valid.".format(parameter, index))

                        # self.synapses[index][mechanism]['namespace_parametrizations'][parameter + identifier_string_addition] = parameter_value

        # # 5.2 Apply varied parameters via namespacing
        # for index, value in self.neurons.items():
        #     self.neurons[index]['namespace_variations'] = {}

        # for index, value in spec.connections.items():
        #     for mechanism in self.synapses[index]['mechanism_list']:
        #         self.synapses[index][mechanism]['namespace_variations'] = {}
        # # 6.0 Save everything needed for reproducing model simulation!
        # # 6.1 Save model equations, structure, and namespacing
        # with open('sim_job1_model.json', 'w') as outfile:
        #     json.dump({'neurons': self.neurons}, outfile)
        #     json.dump({'synapses': self.synapses}, outfile)

#         # 6.2 Save simulator options
#         # with open('sim_ops.json','w') as outfile:
#         #     json.dump(sim_ops, outfile)

        # # 7.0 Create neuron objects
        # for index, value in self.neurons.items():
        #     # TODO then uh...load it if one exists? which involves: 0. satisfying this workflow with attrs of these objects (e.g. Models objects) 1. checking if one exists, 2. diffing any? maybe not?
        #     new_namespace = {}
        #     new_namespace = self.neurons[index]['namespace_parametrizations'].copy()
        #     new_namespace.update(self.neurons[index]['namespace_variations'])
        #     self.neurons[index]['neuron_object'] = NeuronGroup(N=self.neurons[index]['size'],
        #                                                        model=self.neurons[index]['full_neuron_eqns'],
        #                                                        method=sim_ops.solver,
        #                                                        namespace=new_namespace)
        #                                                        # threshold='v > ' + str(sim_ops.spike_detection_threshold),
        #                                                        # refractory=sim_ops.spike_detection_refractory)
        # # 8.0 Create synapse objects
        # for index, value in self.synapses.items():
        #     # need to add all intrinsic mechs
        #     for mechanism in self.synapses[index]['mechanism_list']:
        #         for neuron_index, neuron_value in self.neurons.items():
        #             if self.neurons[neuron_index]['name'] == self.synapses[index]['source']:
        #                 source_object = self.neurons[neuron_index]['neuron_object']
        #             if self.neurons[neuron_index]['name'] == self.synapses[index]['target']:
        #                 target_object = self.neurons[neuron_index]['neuron_object']

                # try:
                #     source_object
                # except NameError:
                #     sys.exit("Synapse number {} has a source neuron {}, but this source neuron does not appear to exist.".format(index, self.synapses[index]['source']))
                # try:
                #     target_object
                # except NameError:
                #     sys.exit("Synapse number {} has a target neuron {}, but this source neuron does not appear to exist.".format(index, self.synapses[index]['target']))

                # new_namespace = {}
                # new_namespace = self.synapses[index][mechanism]['namespace_parametrizations'].copy()
                # new_namespace.update(self.synapses[index][mechanism]['namespace_variations'])
                # self.synapses[index][mechanism]['synapse_object'] = Synapses(source=source_object,
                #                                                              target=target_object,
                #                                                              model=self.synapses[index][mechanism]['full_synapse_eqns'],
                #                                                              namespace=new_namespace)

                # if self.synapses[index][mechanism]['converted_eqns']['connection_eqns'] == '':
                #     # TODO check that this is all-to-all
                #     condition_eqns = None
                # else:
                #     condition_eqns = self.synapses[index][mechanism]['converted_eqns']['connection_eqns']
                # self.synapses[index][mechanism]['synapse_object'].connect(condition=condition_eqns)

#         # # Network has to be collected in the same scope as the synapse and neuron creation?
#         # net = Network(collect())


        # pass

    def convert_mechanism(self, raw_eqns: dict, mech: str, source: str = None, target: str = None, neuron: str = None):

        for group_key, group_value in raw_eqns.items():
            if group_key == 'connection_eqns':
                substituted_eqns[group_key] = group_value
                continue
            elif group_key == 'external_dependencies':
                continue
            # Build an Equations object from the raw_eqns equations so that:
            #     1. we get error-checking and
            #     2. we can use its processing of 'names', 'eq_names', and 'identifiers' to make our own customizations
            # If you can figure out a different way to replace variable names in Equations objects after object
            #     creation, without using insane regular expressions, then do it...

            group_eqns = Equations(raw_eqns[group_key])

            substitutions_dict = {}

            # # 2. in one step, make a new resulting Equations object that includes ALL the name changes in an "exec" kind of way
            # # this is where the magic happens
            # # this is only used for 1. applying our substitutions and 2. using the Equations object as an error-checker
            # # substitution_arguments = str(["{}={}".format(key, value) for key, value in substitutions_dict.items()])

            # # this is also used for making "target_neuron_eqns" maybe?
            substitution_arguments = str(["{}='{}'".format(key, value) for key, value in substitutions_dict.items()])
            substitution_arguments = substitution_arguments.replace('"','')
            substitution_arguments = substitution_arguments.strip('[]')
            exec("substituted_eqns[group_key] = Equations(group_value," + substitution_arguments + ")")

        # find the "current" equation in the 'target_neuron' for use in the NeuronGroups
        # needs to be done BEFORE NeuronGroups are formed
        # need to know how many cells of each source pop there are for this
        # problem: TODO need all params in current as well

        output = {}
        for group_key, group_value in substituted_eqns.items():
            output[group_key] = str(substituted_eqns[group_key])

        return(output)

    def parse_connections_directions(self):
        """
        Insert the population-specific equations of connections that require them (e.g. Synapses in Brian 2) into
        their respective population equations.
        :return:
        """
        for cxn in self.connections.keys():
            directions = cxn.split('->')
            if len(directions) == 1:
                self.connections[cxn]['target'] = directions[0]
            elif len(directions) == 2:
                self.connections[cxn]['source'] = directions[0]
                self.connections[cxn]['target'] = directions[1]

    def load_mechanisms(self):
        """
        Search for mechanism .yaml files in the current working directory and all subdirectories, based on the
        contents of both BrianModel.populations[<all>]['mechanisms'] and BrianModel.connections[<all>]['mechanisms'],
        and load the file contents into, respectively, BrianModel.populations[<all>][<mechanism>]['raw_equations'] and
        BrianModel.connections[<all>][<mechanism>]['raw_equations']. NOT a pure function.
        :return:
        """

        extensions = ['.yaml']

        print("Current working directory is '{}'; searching inside to find mechanism .yaml files.".format(os.getcwd()))

        for pop in self.populations:
            for mech in self.populations[pop]['mechanisms']:
                self.populations[pop][mech]['raw_equations'] = self.traverse_mechanism_files(mech,
                                                                                             extensions)
        for cxn in self.connections:
            for mech in self.connections[cxn]['mechanisms']:
                self.connections[cxn][mech]['raw_equations'] = self.traverse_mechanism_files(mech,
                                                                                             extensions)

    def setup_population_mechanisms(self):
        # Initialize each population's 'full_equations'
        for pop in self.populations:
            self.populations[pop]['full_equations'] = copy.deepcopy(self.populations[pop]['master_equations'])

        for pop in self.populations:
            for mech in self.populations[pop]['mechanisms']:
                # Add each mechanism's equations
                self.populations[pop]['full_equations'] += self.populations[pop][mech]['raw_equations'][
                    'population_equations']
                # TODO current
                # if mech.startswith('i'):
                    # self.synapses[index][mechanism]['current']['name'] = str([value for value in current_object.eq_names
                    #                                                           if value.startswith('I_')][0])
            # Add the corresponding equations from connections targeting this population
            for cxn in self.connections:
                if self.connections[cxn]['target'] is pop:
                    for cxn_mech in self.connections[cxn]['mechanisms']:
                        if self.connections[cxn][cxn_mech]['raw_equations']['target_population_equations']:
                            self.populations[pop]['full_equations'] += \
                                self.connections[cxn][cxn_mech]['raw_equations']['target_population_equations']



        # then add syn to 'current' and 'full_equations'

    def traverse_mechanism_files(self, mechanism: str, extensions: list):
        """
        Internal convenience function for searching the file tree for mechanism files.
        """
        for extension in extensions:
            for root, dirs, files in os.walk(os.getcwd()):
                extended_mechanism = mechanism + extension
                if extended_mechanism in files:
                    mechanism_filename = os.path.join(root, extended_mechanism)
                    print('Loading mechanism file {}'.format(mechanism_filename))
                    with open(mechanism_filename, 'r') as f:
                        output = yaml.load(f)

        if not output:
            sys.exit("Cannot find mechanism file for mechanism named '{}'".format(mechanism))

        return output

    def validate_mechanisms(self):
        for pop in self.populations:
            for mech in self.populations[pop]['mechanisms']:
                if self.populations[pop][mech]['raw_equations']['population_equations']:
                   try:
                       b2.Equations(self.populations[pop][mech]['raw_equations']['population_equations'])
                   except:
                       raise

        for cxn in self.connections:
            for mech in self.connections[cxn]['mechanisms']:
               if self.connections[cxn][mech]['raw_equations']['connection_equations']:
                   try:
                       b2.Equations(self.connections[cxn][mech]['raw_equations']['connection_equations'])
                   except:
                       raise
               if self.connections[cxn][mech]['raw_equations']['target_population_equations']:
                   try:
                       b2.Equations(self.connections[cxn][mech]['raw_equations']['target_population_equations'])
                   except:
                       raise
