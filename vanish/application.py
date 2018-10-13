from argparse import ArgumentParser
from .commands import (List,
                       Connect,
                       UpdateOvpnConfigs,
                       PingServers,
                       Version)
from .utils import ServiceProvider, CacheManager
from .config import config
from .model import GeoJson, OvpnConfigs, ServerContainer


class Vanish(object):
    def __init__(self):
        """Application coordinator.

        Coordinates the link between command line interface and business
        logic classes/command handlers
        """
        self._parser = VanishArgumentParser(
            "vanish",
            description=(
                "a tool to manage connections to IP Vanish servers"
                )
            )

        self._services = self._setupServices(ServiceProvider())
        self._commands = self._setupCommands(ServiceProvider())

    def run(self, args=None):
        """
        Execute a command based on the arguments passed via command line.
        """
        arguments = vars(self._parser.parse_args(args))

        if 'subcommand' in arguments:
            command = "{}.{}".format(arguments['command'],
                                     arguments['subcommand'])
        else:
            command = arguments['command']

        if command in self._commands:
            self._commands[command].execute(arguments)
        else:
            self._parser.print_help()

    def _setupCommands(self, provider):
        provider['list.continents'] = lambda: List(self._services)
        provider['list.countries'] = lambda: List(self._services)
        provider['list.regions'] = lambda: List(self._services)
        provider['list.cities'] = lambda: List(self._services)
        provider['list.servers'] = lambda: List(self._services)

        provider['connect'] = lambda: Connect(self._services)

        provider['sync'] = lambda: UpdateOvpnConfigs(self._services)

        provider['ping'] = lambda: PingServers(self._services)

        provider['version'] = lambda: Version(self._services)

        return provider

    def _setupServices(self, provider):
        provider['config'] = lambda: config

        provider['cache'] = ServiceProvider.singleton(
            lambda: CacheManager(provider['config']['cache.path']))

        provider['servers'] = ServiceProvider.singleton(
            lambda: ServerContainer(
                provider['config']['geojson.cache.path']
                )
            )

        provider['ovpnconfigs'] = lambda: OvpnConfigs(
            provider['config']['ovpn.configs.url'],
            provider['config']['ovpn.configs.path'],
            provider['cache']
            )

        provider['geojson'] = lambda: GeoJson(
            provider['config']['geojson.url'],
            provider['config']['geojson.cache.path'],
            provider['cache']
            )

        return provider


class VanishArgumentParser(ArgumentParser):

    COMMAND = "command"
    SUBCOMMAND = "subcommand"

    def __init__(self, *args, **kwargs):
        super(VanishArgumentParser, self).__init__(*args, **kwargs)

        command = self.add_subparsers(
            dest=self.COMMAND,
            parser_class=ArgumentParser
            )

        ping = command.add_parser('ping', help="ping servers")
        self._addAllServerFilters(ping.add_argument_group('filters'))

        command.add_parser(
            "sync",
            help="sync openvpn config cache with server"
            )

        connect = command.add_parser(
            'connect',
            help='connect to server'
            )
        connect.add_argument(
            'bucket',
            default=None,
            nargs="*"
            )
        self._addAllServerFilters(connect.add_argument_group('filters'))

        list = command.add_parser(
            'list',
            aliases=['ls'],
            help='list locations or servers'
        )
        list.add_argument(
            self.SUBCOMMAND,
            help="default: servers",
            default='servers',
            choices=['servers', 'continents', 'countries', 'regions', 'cities']
            )
        self._addAllServerFilters(list.add_argument_group('filters'))

    def _addAllServerFilters(self, parser):
        self._addContinentsFilter(parser)
        self._addCountriesFilter(parser)
        self._addRegionsFilter(parser)
        self._addCitiesFilter(parser)

    def _addContinentsFilter(self, parser):
        parser.add_argument(
            '--continent',
            action='append',
            dest='continents',
            metavar="",
            help="continent name or code"
        )

    def _addCountriesFilter(self, parser):
        parser.add_argument(
            '--country',
            action='append',
            dest='countries',
            metavar="",
            help="country name or code"
        )

    def _addRegionsFilter(self, parser):
        parser.add_argument(
            '--region',
            action='append',
            dest='regions',
            metavar="",
            help="region name or code"
        )

    def _addCitiesFilter(self, parser):
        parser.add_argument(
            '--city',
            action='append',
            dest='cities',
            metavar="",
            help="city name"
        )
