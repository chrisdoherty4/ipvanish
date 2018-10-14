import unittest
import sys
from .. import application
from io import StringIO


class TestCommands(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = StringIO()
        cls.err = StringIO()
        cls.app = application.Vanish()

    def setUp(self):
        sys.stderr = self.err
        sys.stdout = self.out

    def tearDown(self):
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__

    def test_invalid_command(self):
        with self.assertRaises(SystemExit):
            self.app.run(['invalid-command'])

    def test_list(self):
        self.app.run(['list'])

    def test_list_continents(self):
        self.app.run(['list', 'continents'])

    def test_list_countries(self):
        self.app.run(['list', 'countries'])

    def test_list_regions(self):
        self.app.run(['list', 'regions'])

    def test_list_cities(self):
        self.app.run(['list', 'cities'])

    def test_list_servers(self):
        self.app.run(['list', 'servers'])

    @unittest.skip("Takes too long")
    def test_ping(self):
        self.app.run(['ping'])
