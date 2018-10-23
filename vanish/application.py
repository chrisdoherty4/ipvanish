from argparse import ArgumentParser
from .commands import (List,
                       Connect,
                       UpdateOvpnConfigs,
                       PingServers,
                       Version)
from .utils import ServiceProvider, PersistentCache
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
            description=("a tool to manage connections to IP Vanish servers")
            )

        self._services = ServiceProvider()
        self._setupServices(self._services)
        self._setupCommands(self._services)

    def run(self, args=None):
        arguments = vars(self._parser.parse_args(args))

        if VanishArgumentParser.SUBCOMMAND in arguments:
            command = "cmd.{}.{}".format(
                arguments[VanishArgumentParser.COMMAND],
                arguments[VanishArgumentParser.SUBCOMMAND]
                )
        else:
            command = "cmd.{}".format(arguments[VanishArgumentParser.COMMAND])

        if command in self._services:
            self._services[command].execute(arguments)
        else:
            self._parser.print_help()

    def _setupCommands(self, provider):
        provider.update({
            'cmd.list.continents': lambda p: List(p),
            'cmd.list.countries': lambda p: List(p),
            'cmd.list.regions': lambda p: List(p),
            'cmd.list.cities': lambda p: List(p),
            'cmd.list.servers': lambda p: List(p),
            'cmd.list': lambda p: List(p),
            'cmd.connect': lambda p: Connect(p),
            'cmd.sync': lambda p: UpdateOvpnConfigs(p),
            'cmd.ping': lambda p: PingServers(p),
            'cmd.version': lambda p: Version(p)
            })

    def _setupServices(self, provider):
        provider.update({
            'config': lambda p: config,
            'cache': ServiceProvider.singleton(
                lambda p: PersistentCache(p['config']['cache.path'])
                ),
            'servers': ServiceProvider.singleton(
                lambda p: ServerContainer(p['geojson'])
                ),
            'ovpnconfigs': lambda p: OvpnConfigs(
                p['config']['ovpn.configs.url'],
                p['config']['ovpn.configs.path']
                ),
            'geojson': lambda p: GeoJson(
                p['config']['geojson.url'],
                p['config']['geojson.cache.path']
                ),

            })


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
            nargs="?",
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
