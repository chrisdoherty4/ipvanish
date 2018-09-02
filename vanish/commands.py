import subprocess
import json
import os
import random
import re
import tabulate


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


class Connect(Command):
    """
    Command to connect to the VPN server.
    """

    def execute(self, arguments):
        # TODO: Intelligently select server
        # TODO: Force a GeoJson update.

        if not arguments['server']:
            # TODO: Intelligently select a server
            servers = self._services['servers'].getServers(
                continents=arguments['continents'],
                countries=arguments['countries'],
                regions=arguments['regions'],
                cities=arguments['cities']
                )

            server = random.choice(servers)

            config_file = "{}.ovpn".format(
                "-".join([
                    server['countryCode'],
                    server['hostname'].split('.')[0]])
                .lower())

        else:
            config_file = "{}.ovpn".format(arguments['server'].lower())

        command = [
            'openvpn',
            '--config', os.path.join(
                self._services['config']['ovpn.configs.path'],
                config_file
                ),
            '--cert', self._servces['config']['ovpn.cert']
            ]

        if arguments['auth_user_pass']:
            command.extend(['--auth-user-pass', os.path.abspath(os.path.join(
                os.getcwd(), arguments['auth_user_pass']))])

        subprocess.check_call(
            command, cwd=self._services['config']['ovpn.configs.dir'])


class PingServers(Command):
    def execute(self, arguments):
        servers = self._services['servers'].getServers(
            continents=arguments['continents'],
            countries=arguments['countries'],
            regions=arguments['regions'],
            cities=arguments['cities'])

        print("Pinging servers ...")

        table = []

        for server in servers:
            try:
                response = subprocess.check_output(
                    ['ping', '-c', '1', '-W', '1', server['ip']])

                response_time = re.search(
                    "(?<=time=)([\d\.]+)", response.decode('utf-8'))

                server_handle = "{}-{}".format(server['countryCode'].lower(),
                                               server['hostname'].split('.')[0])

                table.append([
                    server['title'],
                    server_handle,
                    str(server['capacity']) + "%",
                    response_time.group(0) + " ms"
                    ])

            except subprocess.CalledProcessError:
                print("Failed to ping {host}".format(host=server['hostname']))

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
