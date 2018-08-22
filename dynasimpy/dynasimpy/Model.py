from .SimulatorOptions import SimulatorOptions
from .Specification import Specification

# In general, the below is not recommended, but it is specifically recommended by the Brian2 package.
from brian2 import *
# from brian2 import Equations
# from brian2 import NeuronGroup
# from brian2 import Synapses
# import brian2 as b2

# import ipdb

# import json
# import jsonpickle

import os
import re
import sys
# import yaml

class Model:
    def __init__(self, spec: Specification = None, sim_ops: SimulatorOptions = None):
        self.neurons = {}
        self.synapses = {}

        # overall process:
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

        # 1.0 Load and convert connections from specification
        for index, connection in spec.connections.items():
            self.synapses[index] = {}
            self.synapses[index]['direction'] = spec.connections[index]['direction']
            directions = self.synapses[index]['direction'].split('->')
            self.synapses[index]['source'] = directions[0]
            self.synapses[index]['target'] = directions[1]
            self.synapses[index]['mechanism_list'] = spec.connections[index]['mechanism_list']

            for population_index, population_value in spec.populations.items():
                if spec.populations[population_index]['name'] == self.synapses[index]['source']:
                    self.synapses[index]['source_size'] = spec.populations[population_index]['size']
                    continue
                elif spec.populations[population_index]['name'] == self.synapses[index]['target']:
                    self.synapses[index]['target_size'] = spec.populations[population_index]['size']
                    continue

            for mechanism in spec.connections[index]['mechanism_list']:
                self.synapses[index][mechanism] = {}
                self.synapses[index][mechanism]['name'] = mechanism
                self.synapses[index][mechanism]['raw_eqns'] = self.lookup_mechanism(mechanism)
                self.synapses[index][mechanism]['converted_eqns'] = self.convert_mechanism(raw_eqns=self.synapses[index][mechanism]['raw_eqns'],
                                                                                           mech=self.synapses[index][mechanism]['name'],
                                                                                           source=self.synapses[index]['source'],
                                                                                           source_size=self.synapses[index]['source_size'],
                                                                                           target=self.synapses[index]['target'])
                # Only grab current if mechanism prefixed with 'i' like in DynaSim
                if mechanism.startswith('i'):
                    self.synapses[index][mechanism]['current'] = {}
                    # use .eq_names, NOT .names or anything else, so that current will only be identified, once, by its definition (e.g. if an equation uses a current from another mechanism)
                    current_object = Equations(self.synapses[index][mechanism]['converted_eqns']['target_neuron_eqns'])
                    self.synapses[index][mechanism]['current']['name'] = str([value for value in current_object.eq_names
                                                                              if value.startswith('I_')][0])
                    # self.synapses[index][mechanism]['current']['name'] = str([value for value in
                    #                                                           self.synapses[index][mechanism]['converted_eqns']['target_neuron_eqns'].eq_names
                    #                                                           if value.startswith('I_')][0])
                    pass
                # output['current']['equation'] = str([value for key, value in output['target_neuron'].items() if key.startswith('I_')][0])

        # 2.0 Load and convert populations from specification
        for index, population in spec.populations.items():
            # apparently referring to variables/arrays followed by an underscore will refer to the variable without units?
            # http://brian2.readthedocs.io/en/stable/introduction/changes.html?highlight=volts%20seconds
            self.neurons[index] = {}
            self.neurons[index]['name'] = spec.populations[index]['name']
            self.neurons[index]['size'] = spec.populations[index]['size']
            self.neurons[index]['master_eqns'] = spec.populations[index]['master_eqns']
            self.neurons[index]['mechanism_list'] = spec.populations[index]['mechanism_list']

            for mechanism in spec.populations[index]['mechanism_list']:
                self.neurons[index][mechanism] = {}
                self.neurons[index][mechanism]['name'] = mechanism
                self.neurons[index][mechanism]['raw_eqns'] = self.lookup_mechanism(mechanism)
                self.neurons[index][mechanism]['converted_eqns'] = self.convert_mechanism(raw_eqns=self.neurons[index][mechanism]['raw_eqns'],
                                                                                          mech=self.neurons[index][mechanism]['name'],
                                                                                          neuron=self.neurons[index]['name'])
                if mechanism.startswith('i'):
                    self.neurons[index][mechanism]['current'] = {}
                    # use .eq_names, NOT .names or anything else, so that current will only be identified, once, by its definition (e.g. if an equation uses a current from another mechanism)
                    current_object = Equations(self.neurons[index][mechanism]['converted_eqns']['neuron_eqns'])
                    self.neurons[index][mechanism]['current']['name'] = str([value for value in current_object.eq_names
                                                                             if value.startswith('I_')][0])

        # 3.0 Build complete equations string for each neuron type
        for index, value in self.neurons.items():
            self.neurons[index]['full_neuron_eqns'] = ''
            self.neurons[index]['full_neuron_eqns'] += self.neurons[index]['master_eqns'] + '\n'
            items_in_current = []

            # add all contributions from intrinsic mechs
            for mechanism in self.neurons[index]['mechanism_list']:
                self.neurons[index]['full_neuron_eqns'] += self.neurons[index][mechanism]['converted_eqns']['neuron_eqns'] + '\n'
                if mechanism.startswith('i'):
                    items_in_current.append(self.neurons[index][mechanism]['current']['name'])

            # add all contributions from synaptic mechs
            for synapse, synapse_value in self.synapses.items():
                if self.synapses[synapse]['target'] == self.neurons[index]['name']:
                    for mechanism in self.synapses[synapse]['mechanism_list']:
                        self.neurons[index]['full_neuron_eqns'] += self.synapses[synapse][mechanism]['converted_eqns']['target_neuron_eqns'] + '\n'
                        if mechanism.startswith('i'):
                            items_in_current.append(self.synapses[synapse][mechanism]['current']['name'])

            # string magic, i love python
            items_in_current[1:] = ['+' + string for string in items_in_current[1:]]
            self.neurons[index]['full_neuron_eqns'] = self.neurons[index]['full_neuron_eqns'].replace('current', ''.join(items_in_current))

            # TODO try catch Equations errors about being malformed
            try:
                Equations(self.neurons[index]['full_neuron_eqns'])
            except:
                print("Could not interpret neuron population {} as proper Equations:".format(index), sys.exc_info()[0])
                raise

        # 4.0 Build complete equations string for each synapse type
        for index, value in self.synapses.items():
            for mechanism in self.synapses[index]['mechanism_list']:
                self.synapses[index][mechanism]['full_synapse_eqns'] = self.synapses[index][mechanism]['converted_eqns']['synapse_eqns'] + '\n'
                try:
                    Equations(self.synapses[index][mechanism]['full_synapse_eqns'])
                except:
                    print("Could not interpret synapse connection {}, mechanism {} as proper Equations:".format(index, mechanism), sys.exc_info()[0])
                    raise

        # 5.0 Apply modifications from either parametrization or variation by creating namespace_parametrizations and _variations
        # reasons for applying modifications after the initial string interpretation from the spec:
        #   - can keep namespacing changes separate from initial model, built entirely on mech files/raw
        #   - can make explicit what's being varied!
        #   - can easily make full throwaway Equations easily to check for names
        # 5.1 Apply single parametrization via namespacing
        for index, value in spec.populations.items():
            self.neurons[index]['namespace_parametrizations'] = {}

            identifier_string_addition = '_' + self.neurons[index]['name']
            test_master_eqns_object = Equations(self.neurons[index]['master_eqns'])
            test_neuron_eqns_object = Equations(self.neurons[index]['full_neuron_eqns'])

            for parameter, parameter_value in spec.populations[index]['parameters'].items():
                # apply parameters to master_equations
                for name in test_master_eqns_object.names:
                    if name.startswith(parameter):
                        if (   parameter == 'v'
                            or parameter.startswith('N_')
                            or parameter.endswith('_total')
                            or parameter.endswith('_total_post')):
                            sys.exit("The parameter '{}' of neuron index {} is not valid.".format(parameter, index))
                        self.neurons[index]['namespace_parametrizations'][parameter + identifier_string_addition] = str(parameter_value)

                for name in test_neuron_eqns_object.names:
                    if name.startswith(parameter):
                        if (   parameter == 'v'
                            or parameter.startswith('N_')
                            or parameter.endswith('_total')
                            or parameter.endswith('_total_post')):
                            sys.exit("The parameter '{}' of neuron index {} is not valid.".format(parameter, index))

                        self.neurons[index]['namespace_parametrizations'][parameter + identifier_string_addition] = str(parameter_value)

        for index, value in spec.connections.items():
            for mechanism in self.synapses[index]['mechanism_list']:
                self.synapses[index][mechanism]['namespace_parametrizations'] = {}

                identifier_string_addition = ''
                # identifier_string_addition = '_' + self.synapses[index]['source'] + '_' + self.synapses[index]['target']
                test_synapse_eqns_object = Equations(self.synapses[index][mechanism]['full_synapse_eqns'])

                for parameter, parameter_value in spec.connections[index]['parameters'].items():
                    # apply parameters to master_equations
                    for name in test_synapse_eqns_object.names:
                        if name.startswith(parameter):
                            if (   parameter == 'v'
                                or parameter.startswith('N_')
                                or parameter.endswith('_total')
                                or parameter.endswith('_total_post')):
                                sys.exit("The parameter '{}' of synapse index {} is not valid.".format(parameter, index))

                        self.synapses[index][mechanism]['namespace_parametrizations'][parameter + identifier_string_addition] = parameter_value

        # 5.2 Apply varied parameters via namespacing
        for index, value in self.neurons.items():
            self.neurons[index]['namespace_variations'] = {}

        for index, value in spec.connections.items():
            for mechanism in self.synapses[index]['mechanism_list']:
                self.synapses[index][mechanism]['namespace_variations'] = {}
        # 6.0 Save everything needed for reproducing model simulation!
        # 6.1 Save model equations, structure, and namespacing
        with open('sim_job1_model.json', 'w') as outfile:
            json.dump({'neurons': self.neurons}, outfile)
            json.dump({'synapses': self.synapses}, outfile)

        # 6.2 Save simulator options
        # with open('sim_ops.json','w') as outfile:
        #     json.dump(sim_ops, outfile)

        # 7.0 Create neuron objects
        for index, value in self.neurons.items():
            # TODO then uh...load it if one exists? which involves: 0. satisfying this workflow with attrs of these objects (e.g. Models objects) 1. checking if one exists, 2. diffing any? maybe not?
            new_namespace = {}
            new_namespace = self.neurons[index]['namespace_parametrizations'].copy()
            new_namespace.update(self.neurons[index]['namespace_variations'])
            self.neurons[index]['neuron_object'] = NeuronGroup(N=self.neurons[index]['size'],
                                                               model=self.neurons[index]['full_neuron_eqns'],
                                                               method=sim_ops.solver,
                                                               namespace=new_namespace)
                                                               # threshold='v > ' + str(sim_ops.spike_detection_threshold),
                                                               # refractory=sim_ops.spike_detection_refractory)
        # 8.0 Create synapse objects
        for index, value in self.synapses.items():
            # need to add all intrinsic mechs
            for mechanism in self.synapses[index]['mechanism_list']:
                for neuron_index, neuron_value in self.neurons.items():
                    if self.neurons[neuron_index]['name'] == self.synapses[index]['source']:
                        source_object = self.neurons[neuron_index]['neuron_object']
                    if self.neurons[neuron_index]['name'] == self.synapses[index]['target']:
                        target_object = self.neurons[neuron_index]['neuron_object']

                try:
                    source_object
                except NameError:
                    sys.exit("Synapse number {} has a source neuron {}, but this source neuron does not appear to exist.".format(index, self.synapses[index]['source']))
                try:
                    target_object
                except NameError:
                    sys.exit("Synapse number {} has a target neuron {}, but this source neuron does not appear to exist.".format(index, self.synapses[index]['target']))

                new_namespace = {}
                new_namespace = self.synapses[index][mechanism]['namespace_parametrizations'].copy()
                new_namespace.update(self.synapses[index][mechanism]['namespace_variations'])
                self.synapses[index][mechanism]['synapse_object'] = Synapses(source=source_object,
                                                                             target=target_object,
                                                                             model=self.synapses[index][mechanism]['full_synapse_eqns'],
                                                                             namespace=new_namespace)

                if self.synapses[index][mechanism]['converted_eqns']['connection_eqns'] == '':
                    # TODO check that this is all-to-all
                    condition_eqns = None
                else:
                    condition_eqns = self.synapses[index][mechanism]['converted_eqns']['connection_eqns']
                self.synapses[index][mechanism]['synapse_object'].connect(condition=condition_eqns)

        # # Network has to be collected in the same scope as the synapse and neuron creation?
        # net = Network(collect())


        pass

    def convert_mechanism(self, raw_eqns: dict, mech: str, source: str = None, source_size: int = None, target: str = None, neuron: str = None):

        pass
        substituted_eqns = {}
        # # this causes a bunch of bad things to happen, like making changes to output be changes to the originaal attribute of raw_eqns!
        # # substituted_eqns = raw_eqns

        # # Note no underscore at the end
        # # TODO error checking
        # if source != None:
        #     # identifier_string_addition = ''
        #     identifier_string_addition = '_' + source + '_' + target
        #     # identifier_string_addition = '_' + source + '_' + target + '_' + mech
        # elif neuron != None:
        #     identifier_string_addition = ''
        #     # identifier_string_addition = '_' + neuron
            # identifier_string_addition = '_' + neuron + '_' + mech

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
            # # problem: dicts will be reorg'd when changing, so keep what you're iterating over and what you're changing separate
            # # 'names' are just what are defined on the LHS of the equations given.
            # #   - E.g. a parameter that is used in some equations, but is NOT defined in that set of equations, will NOT be a 'name' in the Equations object
            # # 'eq_names' is similar to 'names', but only includes names of equations, NOT parameters
            # for name in group_eqns.names:
            #     # 1. build dict of original IDs and their final IDs
            #     if (name == 'v') or (name.startswith('N_')):
            #         continue
            #     else:
            #         substitutions_dict[name] = name
            #     # elif name.endswith('_total_post'):
            #     #     substitutions_dict[name] = name.replace('_total_post', identifier_string_addition + '_total_post')
            #     # elif name.endswith('_total'):
            #     #     substitutions_dict[name] = name.replace('_total', identifier_string_addition + '_total')
            #     # else:
                #     substitutions_dict[name] = name.replace(name, name + identifier_string_addition)

            # why was this commented
            if 'N_pre' in group_eqns.identifiers:
                substitutions_dict['N_pre'] = source_size

            # if 'external_dependencies' in raw_eqns:
            #     for dependency in raw_eqns['external_dependencies']:
            #         if (name == 'v') or (name.startswith('N_')):
            #             # TODO is this actually necessary?
            #             sys.exit('''You have '{}' indicated as an external dependency in mechanism '{}', but you are using
            #             reserved words in your naming, which is not allowed.'''.format(dependency, mech))
            #         else:
            #             substitutions_dict[dependency] = dependency
            #         # elif name.endswith('_total_post'):
            #         #     substitutions_dict[dependency] = dependency.replace('_total_post', identifier_string_addition + '_total_post')
            #         # elif name.endswith('_total'):
            #         #     substitutions_dict[dependency] = dependency.replace('_total', identifier_string_addition + '_total')
            #         # else:
            #         #     substitutions_dict[dependency] = dependency.replace(dependency, dependency + identifier_string_addition)

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


    def lookup_mechanism(self, mech: str):

        output = {}
        extensions = ['.mech']
        # extensions = ['.yaml']
        # TODO write ugly regex parser to convert DS mech files to dspy type

        # TODO have universal settings path, maybee env var?
        print('Current working directory is {}'.format(os.getcwd()))
        for root, dirs, files in os.walk(os.getcwd()):
            # TODO check if multiple files of same name, give warning that using first one in list (and give list)
            for extension in extensions:
                extended_mech = mech + extension
                if extended_mech in files:
                    mechanism_filename = os.path.join(root, extended_mech)
                    # with open(mechanism_filename) as f:
                    with open(mechanism_filename, 'r') as f:
                        output = f.read()
                        # output = yaml.load(f)

                    # Split newlines into different strings
                    output = re.split(r'\n', output)
                    # Split semicolons into different strings
                    # output = re.split(r'\;', output)
                    for line in output:
                        # Remove all percent-comments, including those after real code
                        output[line] = re.sub(r'%.*$',r'', output[line])

                    # Remove all empty strings in list of strings, from
                    output = list(filter(None, output))
                    pass

        if not mechanism_filename:
            sys.exit("Cannot find mechanism file for mechanism named '{}'".format(mech))

        # output = {}
        # output['name'] = mech
        # output['target_neuron'] = '''
        # tau = 5*ms : second
        # E = -80*mV : volt
        # s_total : 1
        # # N_pre or N_post?
        # # Note: there must be an equation for a variable named 'i'
        # i = -g/N_pre*s_total*(v-E) : amp
        # '''
        # output['synapse'] = TODO
        # output['connection'] = TODO


        # TODO validate mechanism file

        return(output)
