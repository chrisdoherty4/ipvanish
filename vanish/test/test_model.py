import unittest
import tempfile
import shutil
import os
from .. import model, utils


class TestGeoJson(unittest.TestCase):
    def setUp(self):
        self._working_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._working_dir)

    def test_update(self):
        cache = utils.CacheManager({'config.dir': self._working_dir})
        geojson_file = os.path.join(self._working_dir, 'geojson')

        geojson = model.GeoJson(
            "https://www.ipvanish.com/api/servers.geojson",
            geojson_file,
            cache
            )

        geojson.update()


class TestOvpnConfig(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_update(self):
        pass
