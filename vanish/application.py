from argparse import ArgumentParser, RawTextHelpFormatter
from .commands import (ListContinents,
                       ListCountries,
                       ListRegions,
                       ListCities,
                       ListServers,
                       Connect,
                       UpdateOvpnConfigs,
                       PingServers,
                       Version)
from .utils import ServiceProvider, CacheManager
from .config import config
from .model import GeoJson, OvpnConfigs, ServerContainer


class Vanish(object):
    """
    Entrypoint controller for the vanish application.
    """

    def __init__(self):
        self._args = _Args()

        self._services = ServiceProvider()
        self._setupServices()

        self._commands = ServiceProvider()
        self._setupCommands()

    def run(self, args=None):
        """
        Execute a command based on the arguments passed via command line.
        """
        arguments = self._args.run(args)

        if 'subcommand' in arguments:
            command = "{}.{}".format(arguments['command'],
                                     arguments['subcommand'])
        else:
            command = arguments['command']

        if command in self._commands:
            self._commands[command].execute(arguments)
        else:
            self._args.getParser().print_help()

    def _setupCommands(self):
        self._commands['list.continents'] = lambda: ListContinents(
            self._services)

        self._commands['list.countries'] = lambda: ListCountries(
            self._services)

        self._commands['list.regions'] = lambda: ListRegions(self._services)

        self._commands['list.cities'] = lambda: ListCities(self._services)

        self._commands['list.servers'] = lambda: ListServers(self._services)

        self._commands['connect'] = lambda: Connect(self._services)

        self._commands['sync.ovpn-configs'] = lambda: UpdateOvpnConfigs(
            self._services)

        self._commands['ping'] = lambda: PingServers(self._services)

        self._commands['version'] = lambda: Version(self._services)

    def _setupServices(self):
        self._services['config'] = lambda: config

        self._services['cache'] = ServiceProvider.singleton(
            lambda: CacheManager(self._services['config']['cache.path']))

        self._services['servers'] = ServiceProvider.singleton(
            lambda: ServerContainer(
                self._services['config']['geojson.cache.path']
            )
        )

        self._services['ovpnconfigs'] = lambda: OvpnConfigs(
            self._services['config']['ovpn.configs.url'],
            self._services['config']['ovpn.configs.path'],
            self._services['cache']
        )

        self._services['geojson'] = lambda: GeoJson(
            self._services['config']['geojson.url'],
            self._services['config']['geojson.cache.path'],
            self._services['cache']
        )


class _Args(object):
    # TODO: Turn this into an argparser
    """
    Defines the arguments that can be parsed by the vanish application.
    """

    def __init__(self):
        self._parser = ArgumentParser(
            "vanish",
            formatter_class=RawTextHelpFormatter,
            description='Vanish is a tool that helps users on linux connect to IPVanish VPN servers.')

        self._command_parser = self._parser.add_subparsers(dest='command')

        self._addList()
        self._addConnect()
        self._addSyncOvpnConfigs()
        self._addPingServer()
        self._addVersion()

    def run(self, args=None):
        return vars(self._parser.parse_args(args))

    def getParser(self):
        return self._parser

    def _addVersion(self):
        self._command_parser.add_parser(
            'version'
        )

    def _addPingServer(self):
        ping = self._command_parser.add_parser(
            'ping', help='Ping IPVanish servers.')

        filter_group = ping.add_argument_group('filters')
        self._addAllServerFilters(filter_group)

    def _addSyncOvpnConfigs(self):
        configs = self._command_parser.add_parser(
            'sync', help="Perform an IPVanish synchronisation.")

        configs.add_argument(
            'subcommand',
            metavar='SUBCOMMAND',
            choices=['ovpn-configs']
        )

    def _addConnect(self):
        connect_parser = self._command_parser.add_parser(
            'connect',
            help='Connect to an IPVanish server'
        )

        connect_parser.add_argument(
            '--server',
            metavar="SERVER",
            default=None,
        )

        connect_parser.add_argument(
            'bucket',
            default=None,
            nargs="*"
        )

        filter_group = connect_parser.add_argument_group('filters')
        self._addAllServerFilters(filter_group)

    def _addList(self):
        list_parser = self._command_parser.add_parser(
            'list',
            help='Retrieve server locations or generate a full server list'
        )

        list_parser.add_argument(
            'subcommand',
            metavar='SUBCOMMAND',
            default='servers',
            choices=['servers', 'continents', 'countries', 'regions', 'cities'])

        filter_group = list_parser.add_argument_group('filters')
        self._addAllServerFilters(filter_group)

    def _addContinentsFilter(self, parser):
        parser.add_argument(
            '--continent',
            action='append',
            dest='continents',
            metavar='CONTINENT'
        )

    def _addCountriesFilter(self, parser):
        parser.add_argument(
            '--country',
            action='append',
            dest='countries',
            metavar='COUNTRY'
        )

    def _addRegionsFilter(self, parser):
        parser.add_argument(
            '--region',
            action='append',
            dest='regions',
            metavar='REGION'
        )

    def _addCitiesFilter(self, parser):
        parser.add_argument(
            '--city',
            action='append',
            dest='cities',
            metavar='CITY'
        )

    def _addAllServerFilters(self, parser):
        self._addContinentsFilter(parser)
        self._addCountriesFilter(parser)
        self._addRegionsFilter(parser)
        self._addCitiesFilter(parser)
