import os
import tabulate
from .model import Vanish
from .__version__ import VERSION


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


class Version(Command):
    def execute(self, arguments):
        print("Vanish version {}".format(VERSION))


class Connect(Command):
    """
    Command to connect to the VPN server.
    """

    def execute(self, arguments):
        if not arguments['server']:
            print("Selecting a server ...")
            servers = self._services['servers'].getServers(
                continents=arguments['continents'],
                countries=arguments['countries'],
                regions=arguments['regions'],
                cities=arguments['cities']
            )

            if not servers:
                print("No servers available with current filters")
                exit()

            servers = sorted(servers, key=lambda x: x['capacity'])
            servers = Vanish.ping(servers[:20])
            servers = sorted(servers, key=lambda x: x['rtt'])
            server = servers[0]

            config_file = "{}.ovpn".format(
                "-".join([
                    server['countryCode'],
                    server['hostname'].split('.')[0]])
                .lower())
        else:
            config_file = "{}.ovpn".format(arguments['server'].lower())

        print("Selected {} ({}); Capacity {}%; Ping {}ms".format(
            server['title'],
            server['hostname'],
            server['capacity'],
            server['rtt']
        ))

        Vanish.connect(
            os.path.join(
                self._services['config']['ovpn.configs.path'],
                config_file),
            self._services['config']['ovpn.cert'],
            *(arguments['bucket'])
        )


class PingServers(Command):
    def execute(self, arguments):
        servers = self._services['servers'].getServers(
            continents=arguments['continents'],
            countries=arguments['countries'],
            regions=arguments['regions'],
            cities=arguments['cities'])

        print("Pinging servers ...")

        servers = Vanish.ping(servers)

        table = []
        for server in servers:
            server_handle = "{}-{}".format(server['countryCode'].lower(),
                                           server['hostname'].split('.')[0])

            table.append([
                server['title'],
                server_handle,
                str(server['capacity']) + "%",
                str(server['rtt']) + " ms"
            ])

        print(tabulate.tabulate(
            sorted(table),
            headers=["Location", "Handle", "Load", "Response"],
            tablefmt="fancy_grid"))


class UpdateGeoJson(Command):
    def execute(self, arguments):
        print("Updating geojson ...")
        self._services['geojson'].update()
        print("IPVanish GeoJson updated")


class UpdateOvpnConfigs(Command):
    def execute(self, arguments):
        print("Updating configs ...")
        self._services['ovpnconfigs'].update()
        print("Open VPN configs updated.")


class ListContinents(Command):
    """
    List continents command
    """

    def execute(self, arguments):
        continents = self._services['servers'].getContinents()

        headers = ['Code', 'Name']

        print(tabulate.tabulate(
            sorted(continents.items()),
            headers=headers,
            tablefmt="fancy_grid"
        ))


class ListCountries(Command):
    """
    List countries command
    """

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None

        countries = self._services['servers'].getCountries(
            continents=continents)

        headers = ['Code', 'Name']

        print(tabulate.tabulate(
            sorted(countries.items()),
            headers=headers,
            tablefmt="fancy_grid"
        ))


class ListRegions(Command):
    """
    List regions command
    """

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None
        countries = arguments['countries'] if arguments['countries'] else None

        regions = self._services['servers'].getRegions(
            continents=continents, countries=countries)

        headers = ['Code', 'Name']

        print(tabulate.tabulate(
            sorted(regions.items()),
            headers=headers,
            tablefmt="fancy_grid"
        ))


class ListCities(Command):
    """
    List cities command
    """

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None
        countries = arguments['countries'] if arguments['countries'] else None
        regions = arguments['regions'] if arguments['regions'] else None

        cities = self._services['servers'].getCities(
            continents=continents, countries=countries, regions=regions)

        headers = ['Name']

        cities_data = [[c] for c in cities]

        print(tabulate.tabulate(
            sorted(cities_data),
            headers=headers,
            tablefmt="fancy_grid"
        ))


class ListServers(Command):
    """
    List cities command
    """

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None
        countries = arguments['countries'] if arguments['countries'] else None
        regions = arguments['regions'] if arguments['regions'] else None
        cities = arguments['regions'] if arguments['regions'] else None

        servers = self._services['servers'].getServers(
            continents=continents,
            countries=countries,
            regions=regions,
            cities=cities
        )

        headers = ['Continent', 'Country', 'Region', 'City', 'Server']

        server_data = [
            (s['continent'], s['country'], s['region'],
             s['city'], s['hostname'].split(".")[0])
            for s in servers
        ]

        print(tabulate.tabulate(
            sorted(server_data),
            headers=headers,
            tablefmt="fancy_grid"
        ))
