from .commands import (ListContinents,
                       ListCountries,
                       ListRegions,
                       ListCities,
                       ListServers,
                       Connect,
                       UpdateOvpnConfigs,
                       UpdateGeoJson,
                       PingServers)
from .utils import ServiceProvider, CacheManager
from .config import config
from .model import GeoJson, OvpnConfigs, ServerContainer


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
        self._commands['list.continents'] = lambda: ListContinents(
            self._services)

        self._commands['list.countries'] = lambda: ListCountries(
            self._services)

        self._commands['list.regions'] = lambda: ListRegions(self._services)

        self._commands['list.cities'] = lambda: ListCities(self._services)

        self._commands['list.servers'] = lambda: ListServers(self._services)

        self._commands['connect'] = lambda: Connect(self._services)

        self._commands['update-configs'] = lambda: UpdateOvpnConfigs(
            self._services)

        self._commands['update-servers'] = lambda: UpdateGeoJson(
            self._services)

        self._commands['ping'] = lambda: PingServers(self._services)

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
            self._services['config']['ovpnconfigs.url'],
            self._services['config']['ovpnconfigs.cache.path'],
            self._services['cache']
            )

        self._services['geojson'] = lambda: GeoJson(
            self._services['config']['geojson.url'],
            self._services['config']['geojson.cache.path'],
            self._services['cache']
            )
