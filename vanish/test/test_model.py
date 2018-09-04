import unittest
import tempfile
import shutil
import os
import time
from .. import model, utils


class TestGeoJson(unittest.TestCase):
    def setUp(self):
        self.working_dir = tempfile.mkdtemp()
        self.cache = utils.CacheManager(
            os.path.join(self.working_dir, 'cache'))
        self.geojson_file = os.path.join(self.working_dir, 'geojson')

    def tearDown(self):
        shutil.rmtree(self.working_dir)

    def test_update(self):
        geojson = model.GeoJson(
            "https://www.ipvanish.com/api/servers.geojson",
            self.geojson_file,
            self.cache
            )

        current_time = time.time()

        geojson.update()

        self.assertTrue(os.path.exists(self.geojson_file),
                        "No geojson fiel created")

        self.assertLess(current_time, os.path.getmtime(
            self.geojson_file), "Geojson file was not updated")

    def test_badGeoJsonWrite(self):
        geojson = model.GeoJson(
            "https://www.ipvanish.com/api/servers.geojson",
            os.path.join(self.working_dir, "fake", "path"),
            self.cache
            )

        with self.assertRaises(IOError, msg="Success with invalid write path."):
            geojson.update()


class TestOvpnConfig(unittest.TestCase):
    def setUp(self):
        self.working_dir = tempfile.mkdtemp()
        self.cache = utils.CacheManager(
            os.path.join(self.working_dir, 'cache'))
        self.config_path = os.path.join(self.working_dir, 'ovpn')

        os.makedirs(self.config_path)

    def tearDown(self):
        shutil.rmtree(self.working_dir)

    def test_update(self):
        ovpn = model.OvpnConfigs(
            "https://www.ipvanish.com/software/configs/configs.zip",
            self.config_path,
            self.cache
            )

        ovpn.update()

        self.assertGreater(len(os.listdir(self.config_path)),
                           0, "No files unzipped")

# TODO: Write tests for ServerContainer onece it's refactored.
# Intention is to rework it so it does have to worry about exact geojson format
# and instead has it's own expected format.
