import os
import requests
import json
import time
from commands import (ListContinentsCommand,
                      ListCountriesCommand,
                      ListRegionsCommand,
                      ListCitiesCommand,
                      ListServersCommand,
                      ConnectCommand,
                      UpdateOvpnConfigs,
                      PingServersCommand)
from .server import ServerContainer
from .utils import ServiceProvider


class ConfigManager(dict):

    def __init__(self):
        self["config.dir"] = os.path.abspath(os.path.expanduser(
            os.path.join('~', '.config', 'vanish')))

        self["geojson.url"] = "https://www.ipvanish.com/api/servers.geojson"
        self['geojson.cache'] = os.path.join(
            self['config.dir'], 'servers.geojson')
        self['geojson.cache.timeout'] = 30

        self["ovpn.configs.url"] = "https://www.ipvanish.com/software/configs/configs.zip"
        self["ovpn.configs.dir"] = os.path.join(
            self['config.dir'], 'openvpn')
        self['ovpn.configs.timeout'] = 24*60*60  # 1 day in seconds


class CacheManager(object):

    def __init__(self, config):
        """
        # TODO: Decouple individual cache functions from the CachManager.
        The CacheManager doesn't need to know details about caching, just that
        things need caching and to run them based on keys.
        """
        self._config = config

        self._cache_file = os.path.join(
            self._config['config.dir'], 'cache')

        self._cache = {}
        self._loaded = False

        self.read(self._cache_file)

    def loaded(self):
        return self._loaded

    def read(self, path):
        if os.path.exists(path):
            with open(path) as h:
                self._cache = json.loads(h.read())
                self._loaded = True

    def write(self, path):
        with open(path, 'w') as h:
            h.write(json.dumps(self._cache))

    def save(self, key, value):
        self._cache[key] = value
        self.write(self._cache_file)

    def get(self, key):
        if not self._loaded:
            raise RuntimeError(
                "Tried accessing cache value before cache file loaded")

        return self._cache[key]

    def updateGeoJson(self):
        response = requests.get(
            self._config['geojson.url'], allow_redirects=True)

        with open(self._config['geojson.cache'], 'w') as h:
            h.write(response.content)

        self.update('geojson', int(time.time()))


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
        self._services['config'] = ServiceProvider.singleton(
            lambda: ConfigManager())

        self._services['cache'] = ServiceProvider.singleton(
            lambda: CacheManager(self._services['config']))

        self._services['servers'] = ServiceProvider.singleton(
            lambda: ServerContainer(
                self._services['config']['geojson.cache']
                )
            )
