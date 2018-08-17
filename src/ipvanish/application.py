import getpass
import os
from commands import (ListContinentsCommand,
                      ListCountriesCommand,
                      ListRegionsCommand,
                      ListCitiesCommand,
                      ConnectCommand)
from .server import ServerContainer
from .utils import ServiceProvider


class ConfigManager(dict):

    def __init__(self):
        self["config.root"] = os.path.join(
            'home', getpass.getuser(), '.config', 'vanish')

        self["ipvanish.geojson"] = "https://www.ipvanish.com/api/servers.geojson"
        self["ipvanish.config"] = "https://www.ipvanish.com/software/configs/configs.zip"

        self['cache.server.geojson'] = os.path.join(
            self['config.root'], 'servers.geojson')


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
            self._commands.raw(command)(arguments)
        else:
            raise RuntimeError(
                "Something went wrong, no command could be found to execute")

    def _setupCommands(self):
        self._commands['list.continents'] = ListContinentsCommand(
            self._services)
        self._commands['list.countries'] = ListCountriesCommand(self._services)
        self._commands['list.regions'] = ListRegionsCommand(self._services)
        self._commands['list.cities'] = ListCitiesCommand(self._services)
        self._commands['connect'] = ConnectCommand(self._services)

    def _setupServices(self):
        self._services['config'] = ServiceProvider.singleton(
            lambda: ConfigManager())

        self._services['server.container'] = ServiceProvider.singleton(
            lambda: ServerContainer(
                self._services['config']['cache.server.geojson']
                )
            )
