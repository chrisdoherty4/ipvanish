import unittest
import tempfile
from ..vanish import model, utils


class TestGeoJson(unittest.TestCase):
    def setUp(self):
        self._working_dir = tempfile.mkdtemp()
        self._cache = utils.CacheManager()
        self._config = {
            'config.dir': self._Working_dir
        }

    def testUpdate(self):
        geojson = model.GeoJson(
            "https://www.ipvanish.com/api/servers.geojson",
            self._working_dir,
            utils.CacheManager({'config.dir': self._working_dir})
            )

        geojson.update()
