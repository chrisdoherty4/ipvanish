import hashlib
import json
import os


class ServiceProvider(dict):
    # TODO: Comment class
    class _Singleton(object):
        def __init__(self, callback):
            self._instance = callback()

        def __call__(self):
            return self._instance

    def __init__(self, *args, **kwargs):
        super(ServiceProvider, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        return super(ServiceProvider, self).__getitem__(key)()

    def __setitem__(self, key, value):
        if not callable(value):
            raise ValueError("Value must be callable")

        super(ServiceProvider, self).__setitem__(key, value)

    def raw(self, key):
        return super(ServiceProvider, self).__getitem__(key)

    @staticmethod
    def singleton(callback):
        return ServiceProvider._Singleton(callback)


class CacheManager(object):

    def __init__(self, config):
        """
        The CacheManager doesn't need to know details about caching, just that
        things need caching and to run them based on keys.
        """
        self._config = config

        self._cache_file = os.path.join(
            self._config['config.dir'], 'cache')

        self._cache = {}
        self._loaded = False

        self.load(self._cache_file)

    def loaded(self):
        return self._loaded

    def load(self, path):
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


def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)

    return sha256.hexdigest()
