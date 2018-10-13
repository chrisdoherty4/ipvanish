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
        print("Updating server status.")
        self._services['geojson'].update()

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
        print("Updating server status.")
        self._services['geojson'].update()

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


class List(Command):
    def execute(self, args):
        subcommand = args["subcommand"]

        if subcommand == "continents":
            self._continents()
            exit(0)

        filters = {
            "continents": args['continents'] if args['continents'] else None,
            "countries": args['countries'] if args['countries'] else None,
            "regions": args['regions'] if args['regions'] else None,
            "cities": args['cities'] if args['cities'] else None,
            }

        if subcommand == "countries":
            self._countries(**filters)
        elif subcommand == "regions":
            self._regions(**filters)
        elif subcommand == "cities":
            self._cities(**filters)
        else:
            self._servers(**filters)

    def _continents(self):
        continents = self._services['servers'].getContinents()

        headers = ['Code', 'Name']

        print(tabulate.tabulate(
            sorted(continents.items()),
            headers=headers,
            tablefmt="fancy_grid"
        ))

    def _countries(self, **filters):
        countries = self._services['servers'].getCountries(**filters)

        headers = ['Code', 'Name']

        print(tabulate.tabulate(
            sorted(countries.items()),
            headers=headers,
            tablefmt="fancy_grid"
        ))

    def _regions(self, **filters):
        regions = self._services['servers'].getRegions(**filters)

        headers = ['Code', 'Name']

        print(tabulate.tabulate(
            sorted(regions.items()),
            headers=headers,
            tablefmt="fancy_grid"
        ))

    def _cities(self, **filters):
        cities = self._services['servers'].getCities(**filters)

        headers = ['Name']

        cities_data = [[c] for c in cities]

        print(tabulate.tabulate(
            sorted(cities_data),
            headers=headers,
            tablefmt="fancy_grid"
        ))

    def _servers(self, **filters):
        servers = self._services['servers'].getServers(**filters)

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
