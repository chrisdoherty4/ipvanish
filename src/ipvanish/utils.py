

class ServiceProvider(dict):

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
