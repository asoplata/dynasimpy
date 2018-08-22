class Specification:
    def __init__(self):
        self.populations = {}
        self.connections = {}

    def create_population(self, index: int=None):
        # TODO: error checking for if index doesn't equal existing index +1
        # TODO test that using integers for indices here doesn't break anything
        # index_str = str(index)
        self.populations[index] = {}
        self.populations[index]['name'] = None
        self.populations[index]['size'] = int()
        self.populations[index]['equations'] = None
        self.populations[index]['mechanism_list'] = []
        self.populations[index]['parameters'] = {}

    def create_connection(self, index: int=None, direction: str={}):
        # TODO: error checking for if index doesn't equal existing index +1
        # TODO test that using integers for indices here doesn't break anything
        # index_str = str(index)
        self.connections[index] = {}
        self.connections[index]['direction'] = None
        self.connections[index]['mechanism_list'] = []
        self.connections[index]['parameters'] = {}

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
