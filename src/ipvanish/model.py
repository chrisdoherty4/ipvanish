import requests
import time
import os
import tempfile
import zipfile
import re
import shutil


class GeoJson(object):
    def __init__(self, url, cache_path, cache):
        self._cache = cache
        self._url = url
        self._cache_path = cache_path

    def update(self):
        # TODO: Consider adding in a configurable geojson cache timeout
        response = requests.get(self._url, allow_redirects=True)

        with open(self._cache_path, 'w') as h:
            h.write(response.content)

        self._cache.save('geojson', int(time.time()))


class OvpnConfigs(object):
    def __init__(self, url, path, cache):
        self._url = url
        self._path = path
        self._cache = cache

    def update(self):
        working_dir = tempfile.mkdtemp()

        if os.path.exists(self._path):
            shutil.rmtree(self._path)

        response = requests.get(self._url)

        new_configs = os.path.join(working_dir, 'configs.zip')

        with open(new_configs, 'w') as h:
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
