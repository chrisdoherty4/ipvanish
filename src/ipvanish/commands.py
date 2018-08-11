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


class ListCountriesCommand(object):
    '''
    List countries command
    '''

    def __init__(self, server_container):
        self._server_container = server_container

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None

        countries = self._server_container.getCountries(continents=continents)

        print(countries)


class ListRegionsCommand(object):
    '''
    List regions command
    '''

    def __init__(self, server_container):
        self._server_container = server_container

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None
        countries = arguments['countries'] if arguments['countries'] else None

        regions = self._server_container.getRegions(
            continents=continents, countries=countries)

        print(regions)


class ListCitiesCommand(object):
    '''
    List cities command
    '''

    def __init__(self, server_container):
        self._server_container = server_container

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None
        countries = arguments['countries'] if arguments['countries'] else None
        regions = arguments['regions'] if arguments['regions'] else None

        cities = self._server_container.getCities(
            continents=continents, countries=countries, regions=regions)

        print(cities)
