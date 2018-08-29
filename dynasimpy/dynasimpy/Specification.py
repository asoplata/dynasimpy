import ujson as json

class Specification:
    def __init__(self):
        self.populations = {}
        self.connections = {}

    def create_population(self, name: str, size: int, master_equations: str, mechanisms:list = None,
                          parameters:list = None):
        """
        This adds a new population entry to the dynasimpy.Specification.populations dictionary. Use this to add,
        e.g., a new type of neurons to your model. Obviously, this is not a 'pure' function.

        :param name: Name of the population.
        :type name: str
        :param size: How large the population is, e.g. number of neurons.
        :type size: int
        :param master_equations: The equations for a population which can't be broken down into mechanism files.
        :type master_equations: str
        :param mechanisms: Optional, the base filenames (i.e., without the ".yaml" file extension) of the mechanisms
        you want to use.
        :type mechanisms: list
        :param parameters: Optional, custom values you want to use for a specific parameter in a mechanism instead of
        that mechanism's default value. The syntax for specifying a non-default parameter here is: [<
        :type parameters: list
        :return:
        """

        # The below checks ensure a new list is used for empty default arguments each time the function is called.
        if mechanisms is None:
            mechanisms = []
        if parameters is None:
            parameters = []

        # The below arguments are REQUIRED:
        self.populations[name] = {}
        self.populations[name]['size'] = size
        self.populations[name]['master_equations'] = master_equations

        # The below arguments are optional:
        self.populations[name]['mechanisms'] = mechanisms
        self.populations[name]['parameters'] = parameters

    def create_connection(self, direction: str, mechanisms:list, parameters:list = None):
        """
        This adds a new connection entry to the dynasimpy.Specification.connections dictionary. Use this to add,
        e.g., a new type of synapse or non-synapse connection to your model. Obviously, this is not a 'pure' function.

        :param direction: String specifying the source and target population names of the connection,
        e.g. 'I->E' where 'I' is the source population, and 'E' the target. If your connection mechanism only has a
        target population (e.g. PoissonInput), then just specify the target population name, e.g. 'E'.
        :type direction: str
        :param mechanisms: The base filenames (i.e., without the ".yaml" file extension) of the mechanisms you want
        to use. Note that this is optional for populations, but REQUIRED for connections, since connections are more
        complicated.
        :type mechanisms: list
        :param parameters: Optional, custom values you want to use for a specific parameter in a mechanism instead of
        that mechanism's default value.
        :type parameters: list
        :return:
        """

        if parameters is None:
            parameters = []

        # The below arguments are REQUIRED:
        self.connections[direction] = {}
        self.connections[direction]['mechanisms'] = mechanisms

        # The below arguments are optional:
        self.connections[direction]['parameters'] = parameters

    def load_from_json(self):
        # TODO
        x = 2
