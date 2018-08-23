from commands import (ListContinentsCommand,
                      ListCountriesCommand,
                      ListRegionsCommand,
                      ListCitiesCommand,
                      ListServersCommand,
                      ConnectCommand,
                      UpdateOvpnConfigs,
                      PingServersCommand)
from .server import ServerContainer
from .utils import ServiceProvider, CacheManager
from .config import config


class Vanish(object):
    """
    Entrypoint controller for the vanish application.
    """

    def __init__(self):
        self._services = ServiceProvider()
        self._setupServices()

        self._commands = ServiceProvider()
        self._setupCommands()

    def run(self, command, arguments):
        """
        Execute a command based on the arguments passed via command line.
        """
        if command in self._commands:
            self._commands[command].execute(arguments)
        else:
            raise RuntimeError(
                "No command could be found to execute for '{}'".format(command))

    def _setupCommands(self):
        self._commands['list.continents'] = lambda: ListContinentsCommand(
            self._services)
        self._commands['list.countries'] = lambda: ListCountriesCommand(
            self._services)
        self._commands['list.regions'] = lambda: ListRegionsCommand(
            self._services)
        self._commands['list.cities'] = lambda: ListCitiesCommand(
            self._services)
        self._commands['list.servers'] = lambda: ListServersCommand(
            self._services)

        self._commands['connect'] = lambda: ConnectCommand(self._services)

        self._commands['update-configs'] = lambda: UpdateOvpnConfigs(
            self._services)

        self._commands['ping'] = lambda: PingServersCommand(self._services)

    def _setupServices(self):
        self._services['config'] = lambda: config

        self._services['cache'] = ServiceProvider.singleton(
            lambda: CacheManager(self._services['config']))

        self._services['servers'] = ServiceProvider.singleton(
            lambda: ServerContainer(
                self._services['config']['geojson.cache']
                )
            )
