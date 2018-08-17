import subprocess


class Command(object):
    """
    An interface to command objects
    """

    def __init__(self, services):
        super(Command, self).__init__()
        self._services = services

    def __call__(self, arguments):
        self.execute(arguments)

    def execute(self, arguments):
        raise NotImplementedError()


class ConnectCommand(Command):
    """
    Command to connect to the VPN server.
    """

    def execute(self, arguments):
        # p = subprocess.call([
        #         'openvpn',
        #         '--config',
        #         '/media/hdd1/Downloads/ipvanish/ipvanish-UK-London-lon-a68.ovpn'
        #         ], cwd="/media/hdd1/Downloads/ipvanish")
        #
        # print(p)

        print(self._services['config']['cache.server.geojson'])


class ListContinentsCommand(Command):
    """
    List continents command
    """

    def execute(self, arguments):
        continents = self._services['servers'].getContinents()
        print(continents)


class ListCountriesCommand(Command):
    """
    List countries command
    """

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None

        countries = self._services['servers'].getCountries(
            continents=continents)

        print(countries)


class ListRegionsCommand(Command):
    """
    List regions command
    """

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None
        countries = arguments['countries'] if arguments['countries'] else None

        regions = self._services['servers'].getRegions(
            continents=continents, countries=countries)

        print(regions)


class ListCitiesCommand(Command):
    """
    List cities command
    """

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None
        countries = arguments['countries'] if arguments['countries'] else None
        regions = arguments['regions'] if arguments['regions'] else None

        cities = self._services['servers'].getCities(
            continents=continents, countries=countries, regions=regions)

        print(cities)
