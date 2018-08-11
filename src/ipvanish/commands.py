class Command(object):
    '''
    An interface to command objects
    '''

    def execute(self, arguments):
        raise NotImplementedError()


class ListContinentsCommand(object):
    '''
    List continents command
    '''

    def __init__(self, server_container):
        self._server_container = server_container

    def execute(self, arguments):
        continents = self._server_container.getContinents()
        print(continents)
