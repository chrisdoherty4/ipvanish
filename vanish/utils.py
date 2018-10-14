import hashlib
import json


class ServiceProvider(dict):
    class _Singleton(object):
        def __init__(self, callable):
            self._instance = None
            self._callable = callable

        def __call__(self):
            if not self._instance:
                self._instance = self._callable()

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


class PersistentCache(dict):

    def __init__(self, cache_path):
        """A manager for caching arbirary data.

        :param cache_path: Path to the file we should use for caching.
        """
        self._cache_path = cache_path

        try:
            with open(cache_path) as h:
                self = json.loads(h.read())
        except IOError() as e:
            print("Could not open cache file {}".format(e))
            raise

    def _write(self):
        with open(self._cache_path, 'w') as h:
            h.write(json.dumps(self))

    def __setattr__(self, key, value):
        super(PersistentCache, self).__setattr__(key, value)
        self._write()

    def ___delattr__(self, key):
        super(PersistentCache, self).__delattr__(key)
        self._write()


def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)

    return sha256.hexdigest()
