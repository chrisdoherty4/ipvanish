import requests
import time
import os
import tempfile
import zipfile
import re
import shutil
import json
import subprocess


class GeoJson(object):
    def __init__(self, url, cache_path, cache):
        self._cache = cache
        self._url = url
        self._cache_path = cache_path

    def update(self):
        # TODO: Consider adding in a configurable geojson cache timeout
        response = requests.get(self._url, allow_redirects=True).json()

        # TODO: Move code out into the GeoJson class when it's made

        # Extract the properties of the geojson
        servers = []
        for server in response:
            del server['properties']['marker-color']
            del server['properties']['marker-cluster-small']
            if server['properties']['countryCode'] == "GB":
                server['properties']["countryCode"] = "UK"

            servers.append(server['properties'])

        with open(self._cache_path, 'w') as h:
            json.dump(servers, h, indent=4)

        self._cache.save('geojson', int(time.time()))


class OvpnConfigs(object):
    def __init__(self, url, path, cache):
        """Consructor.

        :param url: URL ovpn configs zip file.
        :param path: Path to write ovpn configs.
        :param cache: A CacheManager instance.
        """
        self._url = url
        self._path = path
        self._cache = cache

    def update(self):
        working_dir = tempfile.mkdtemp()

        if os.path.exists(self._path):
            shutil.rmtree(self._path)

        response = requests.get(self._url)

        new_configs = os.path.join(working_dir, 'configs.zip')

        with open(new_configs, 'wb') as h:
            h.write(response.content)

        with zipfile.ZipFile(new_configs, 'r') as zip:
            zip.extractall(self._path)

        for file in os.listdir(self._path):
            if "ovpn" in file:
                parts = re.search(
                    '^ipvanish-([A-Z]{2})-.+-([a-z]{3}-[a-c]{1}[0-9]{2}.ovpn)$',
                    file
                )
                dest = "-".join([parts.group(1), parts.group(2)]).lower()

                os.rename(
                    os.path.join(self._path, file),
                    os.path.join(self._path, dest)
                )

        shutil.rmtree(working_dir)

        self._cache.save('ovpnconfigs', time.time())


class Vanish(object):
    @staticmethod
    def connect(config_file, ca_file, *kargs):
        """Connect to IPVanishs servers.

        :param config_file: The ovpn configuration file
        :param ca_file: The certificate file for IPVanishs servers.
        :param *kargs: Any additional arguments to pass to openvpn command.
        """
        command = [
            'openvpn',
            '--config', config_file,
            '--ca', ca_file
        ]

        command.extend(kargs)

        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            print("Failed to run openvpn command:")
            print("\t" + " ".join(command))
        except KeyboardInterrupt:
            print("Disconnected")

    @staticmethod
    def ping(servers):
        for i, server in enumerate(servers):
            try:
                response = subprocess.check_output(
                    ['ping', '-c', '1', '-W', '1', server['ip']])

                response_time = re.search(
                    "(?<=time=)([\d\.]+)", response.decode('utf-8'))

                servers[i]['rtt'] = float(response_time.group(0))

            except subprocess.CalledProcessError:
                print("Failed to ping {}".format(server['hostname']))

        return servers


class ServerContainer(object):
    '''
    A container that wraps server information and is queryable.
    '''

    def __init__(self, server_json_path):
        """Constructor.
        """
        with open(server_json_path, 'r') as h:
            self._servers = json.load(h)

    def getServers(self,
                   continents=None,
                   countries=None,
                   regions=None,
                   cities=None):
        '''
        Retrieve a list of servers and their associated information.

        You can optionally filter the list using the continents, countries,
        regions, and cities parameters.

        :param continents: A list of continent names or codes
        :param countries: A list of country names or codes
        :param regions: A list of region names, codes, or abbreviations
        :param cities: A list of city names
        :return: A list of servers.
        '''
        servers = self._servers

        if continents:
            servers = self._filterContinents(servers, continents)

        if countries:
            servers = self._filterCountries(servers, countries)

        if regions:
            servers = self._filterRegions(servers, regions)

        if cities:
            servers = self._filterCities(servers, cities)

        return list(servers)

    def getContinents(self):
        '''
        Retrieve a dictionary of continents.

        :return: A dictionary of continents {code: name}
        '''
        continents = {}

        for s in self._servers:
            if s['continentCode'] not in continents:
                continents[s['continentCode']] = s['continent']

        return continents

    def getCountries(self, continents=None):
        '''
        Retrieve a dictionary of countries.

        :param continents: A list of continent names or codes
        :return: A dictionary of countries {code: name}
        '''
        servers = self._servers

        if continents:
            servers = self._filterContinents(servers, continents)

        countries = {}

        for s in servers:
            if s['countryCode'] not in countries:
                countries[s['countryCode']] = s['country']

        return countries

    def getRegions(self, continents=None, countries=None):
        '''
        Retrieve a dictionary of regions.

        :param continents: A list of continent names or codes
        :param countries: A list of country names of codes
        :return: A dictionary of regions {code: name}
        '''
        servers = self._servers

        if continents:
            servers = self._filterContinents(servers, continents)

        if countries:
            servers = self._filterCountries(servers, countries)

        regions = {}

        for s in servers:
            if s['regionCode'] not in regions:
                regions[s['regionCode']] = s['region']

        return regions

    def getCities(self, continents=None, countries=None, regions=None):
        '''
        Retrieve cities with optional filters.

        Filters can combin the name/code values.

        :param continents: A list of continent names or codes
        :param countries: A list of country names of codes
        :param regions: A list of region names, codes, or abbreviations
        :return: A unique set of cities.
        '''
        servers = self._servers

        if continents:
            servers = self._filterContinents(servers, continents)

        if countries:
            servers = self._filterCountries(servers, countries)

        if regions:
            servers = self._filterRegions(servers, regions)

        return set([server['city'] for server in servers])

    def _filterContinents(self, servers, continents):
        return filter(lambda s: s['continent'] in continents or s['continentCode'] in continents, servers)

    def _filterCountries(self, servers, countries):
        return filter(lambda s: s['country'] in countries or s['countryCode'] in countries, servers)

    def _filterRegions(self, servers, regions):
        return filter(lambda s: s['region'] in regions or s['regionCode'] in regions or s['regionAbbr'] in regions, servers)

    def _filterCities(self, servers, cities):
        return filter(lambda x: x['city'] in cities, servers)
