import ujson as json


class Specification:
    def __init__(self, filename:str = None):

        if filename:
            print('TODO')
        else:
            self.populations = {}
            self.connections = {}

    def create_population(self, name: str, size: int, master_equations: str, mechanisms: list = None):
        """
        Add a new population entry to the Specification.populations dictionary. Use this to add,
        e.g., a new type of neurons to your model. This is NOT a 'pure' function (i.e., it has state changes/"side
        effects").

        :param name: Name of the population.
        :type name: str
        :param size: How large the population is, e.g. number of neurons.
        :type size: int
        :param master_equations: The equations for a population which can't be broken down into mechanism files.
        :type master_equations: str
        :param mechanisms: Optional, the base file names (i.e., without the ".yaml" file extension) of the mechanisms
        you want to use.
        :type mechanisms: list
        :return:
        """

        # The below checks ensure a new list is used for empty default arguments each time the function is called.
        if mechanisms is None:
            mechanisms = []

        # The below arguments are REQUIRED:
        self.populations[name] = {
            'size': size,
            'master_equations': master_equations
        }

        # The below arguments are optional:
        self.populations[name]['mechanisms'] = mechanisms

    def create_connection(self, direction: str, mechanisms: list):
        """
        Add a new connection entry to the Specification.connections dictionary. Use this to add,
        e.g., a new type of synapse or non-synapse connection to your model. This is NOT a 'pure' function (i.e., it has
        state changes/"side effects").

        :param direction: String specifying the source and target population names of the connection,
        e.g. 'I->E' where 'I' is the source population, and 'E' the target. If your connection mechanism only has a
        target population (e.g. PoissonInput), then just specify the target population name, e.g. 'E'.
        :type direction: str
        :param mechanisms: The base file names (i.e., without the ".yaml" file extension) of the mechanisms you want
        to use. Note that this is optional for populations, but REQUIRED for connections, since connections are more
        complicated.
        :type mechanisms: list
        :return:
        """

        # The below arguments are REQUIRED:
        self.connections[direction] = {
            'mechanisms': mechanisms
        }

    def load_from_json(self):
        # TODO
        x = 2
