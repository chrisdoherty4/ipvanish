from commands import (ListContinentsCommand,
                      ListCountriesCommand,
                      ListRegionsCommand,
                      ListCitiesCommand)
from argparse import ArgumentParser, RawTextHelpFormatter
from server import ServerContainer


class Vanish(object):
    '''
    Entrypoint controller for the vanish application.
    '''

    def __init__(self, argument_parser):
        self._parser = argument_parser

        # TODO: Handle downloading and caching of the geojson.
        self._server_container = ServerContainer(
            "/home/chrisdoherty/Downloads/servers.geojson")

        self._commands = {}
        self._commands['list.continents'] = ListContinentsCommand(
            self._server_container)
        self._commands['list.countries'] = ListCountriesCommand(
            self._server_container)
        self._commands['list.regions'] = ListRegionsCommand(
            self._server_container)
        self._commands['list.cities'] = ListCitiesCommand(
            self._server_container)

    def execute(self, args=None):
        '''
        Execute a command based on the arguments passed via command line.
        '''
        arguments = self._parser.parse_args(args)

        if arguments.subcommand:
            command_key = "{}.{}".format(
                arguments.command, arguments.subcommand)
        else:
            command_key = arguments.command

        arguments = vars(arguments)
        del arguments['command']
        del arguments['subcommand']

        if self._commands[command_key]:
            self._commands[command_key].execute(arguments)
        else:
            raise RuntimeError(
                "Something went wrong, no command could be found to execute")


class VanishArgumentParser(object):
    '''
    Defines the arguments that can be parsed by the vanish application.
    '''

    def __init__(self):
        self._parser = ArgumentParser(
            "vanish",
            formatter_class=RawTextHelpFormatter,
            description='Vanish is a tool that helps users on linux connect to IPVanish VPN servers.')

        self._command_parser = self._parser.add_subparsers(dest='command')

        self._addListParser()

    def parse_args(self, args=None):
        return self._parser.parse_args(args)

    def _addListParser(self):
        list_parser = self._command_parser.add_parser(
            'list',
            description='Retrieve server locations or generate a full server list'
            )

        list_parser.add_argument(
            'subcommand',
            metavar='SUBCOMMAND',
            nargs='?',
            default='servers',
            choices=['servers', 'continents', 'countries', 'regions', 'cities'])

        filter_group = list_parser.add_argument_group('Filters')
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
