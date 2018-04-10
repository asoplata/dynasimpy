class Specification:
    def __init__(self):
        self.populations = {}
        self.connections = {}

    def create_population(self, index: int=None):
        # TODO: error checking for if index doesn't equal existing index +1
        index_str = str(index)
        self.populations[index_str] = {}
        self.populations[index_str]['name'] = None
        self.populations[index_str]['size'] = int()
        self.populations[index_str]['equations'] = None
        self.populations[index_str]['mechanism_list'] = []
        self.populations[index_str]['parameters'] = {}

    def create_connection(self, index: int=None, direction: str={}):
        # TODO: error checking for if index doesn't equal existing index +1
        index_str = str(index)
        self.connections[index_str] = {}
        self.connections[index_str]['direction'] = None
        self.connections[index_str]['mechanism_list'] = []
        self.connections[index_str]['parameters'] = {}

    def load_from_json(self):
        # TODO
        x = 2

    def validate_spec(self):
        """TODO: Docstring for validate_spec.
        :returns: TODO

        """
        for key, value in self.connections.items():
            if isinstance(self.connections[key]['mechanism_list'], str):
                self.connections[key]['mechanism_list'] = [self.connections[key]['mechanism_list']]





        return(self)
