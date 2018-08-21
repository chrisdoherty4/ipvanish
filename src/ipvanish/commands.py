import subprocess
import json
import os
import random
import requests
import shutil
import zipfile
import re
import time
from .utils import sha256_checksum

"""
TODO: Create commands:
    * PingServersCommand
    * WriteConfigCommand
    * ShowServerStatusCommand
    * ListServerCapacitiesCommand
    *
"""


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
                "-".join([server['countryCode'], server['hostname'].split('.')[0]]).lower())

        else:
            config_file = "{}.ovpn".format(arguments['server'].lower())

        command = ['openvpn', '--config', os.path.join(
            self._services['config']['ovpn.configs.dir'], config_file)]

        if arguments['auth_user_pass']:
            command.extend(['--auth-user-pass', os.path.abspath(os.path.join(
                os.getcwd(), arguments['auth_user_pass']))])

        subprocess.check_call(
            command, cwd=self._services['config']['ovpn.configs.dir'])


class PingServersCommand(Command):
    def execute(self, arguments):
        servers = self._services['servers'].getServers(
            continents=arguments['continents'],
            countries=arguments['countries'],
            regions=arguments['regions'],
            cities=arguments['cities'])

        print("Pinging servers ...")

        for server in servers:
            try:
                response = subprocess.check_output(
                    ['ping', '-c', '1', '-W', '1', server['ip']])

                response_time = re.search(
                    "time=(.*)", response)

                server_name = "{}-{}".format(server['countryCode'].lower(),
                                             server['hostname'].split('.')[0])

                print("\033[1m{} ({})\033[0m".format(
                    server['title'],
                    server_name))
                print("  Load: {}%; Response {}".format(
                    server['capacity'],
                    response_time.group(0)))

            except subprocess.CalledProcessError:
                print("Failed to ping {host}".format(host=server['hostname']))


class UpdateOvpnConfigs(Command):
    """
    Updates the ovpn configurations with the latest from IPVanish.
    """

    def execute(self, arguments):
        response = requests.get(self._services['config']['ovpn.configs.url'])

        configs_zip = os.path.join(
            self._services['config']['config.dir'], 'configs.zip')
        configs_zip_prev = os.path.join(
            self._services['config']['config.dir'], 'configs.zip.prev')

        with open(configs_zip, 'w') as h:
            h.write(response.content)

        # If there is no previous configs zip, or the previous config zip exists
        # and the sha sums between the latest and old are different update
        # the configs.
        if ((os.path.exists(configs_zip_prev)
                and sha256_checksum(configs_zip) != sha256_checksum(configs_zip_prev))
                or not os.path.exists(configs_zip_prev)):
            shutil.rmtree(self._services['config']['ovpn.configs.dir'])

            with zipfile.ZipFile(configs_zip, 'r') as zip:
                zip.extractall(self._services['config']['ovpn.configs.dir'])

            os.rename(configs_zip, configs_zip_prev)

            for file in os.listdir(self._services['config']['ovpn.configs.dir']):
                if "ovpn" in file:
                    parts = re.search(
                        '^ipvanish-([A-Z]{2})-.+-([a-z]{3}-[a-c]{1}[0-9]{2}.ovpn)$',
                        file
                        )
                    dest = "-".join([parts.group(1), parts.group(2)]).lower()

                    os.rename(
                        os.path.join(
                            self._services['config']['ovpn.configs.dir'], file),
                        os.path.join(
                            self._services['config']['ovpn.configs.dir'], dest)
                        )

            self._services['cache'].save('ovpn.configs', time.time())
        else:
            os.remove(configs_zip)


class ListContinentsCommand(Command):
    """
    List continents command
    """

    def execute(self, arguments):
        continents = self._services['servers'].getContinents()

        print(json.dumps(continents, indent=4, sort_keys=True))


class ListCountriesCommand(Command):
    """
    List countries command
    """

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None

        countries = self._services['servers'].getCountries(
            continents=continents)

        print(json.dumps(countries, indent=4, sort_keys=True))


class ListRegionsCommand(Command):
    """
    List regions command
    """

    def execute(self, arguments):
        continents = arguments['continents'] if arguments['continents'] else None
        countries = arguments['countries'] if arguments['countries'] else None

        regions = self._services['servers'].getRegions(
            continents=continents, countries=countries)

        print(json.dumps(regions, indent=4, sort_keys=True))


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

        print(json.dumps(list(cities), indent=4, sort_keys=True))


class ListServersCommand(Command):
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

        print(json.dumps(list(servers), indent=4, sort_keys=True))
