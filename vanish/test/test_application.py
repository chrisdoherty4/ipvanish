import unittest
import sys
from .. import application
from io import StringIO


class TestCommands(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = StringIO()
        cls.err = StringIO()

    def setUp(self):
        sys.stderr = self.err

    def test_invalidCommand(self):
        app = application.Vanish()

        with self.assertRaises(SystemExit):
            app.run(['invalid-command'])

    def test_incompleteList(self):
        app = application.Vanish()

        with self.assertRaises(SystemExit):
            app.run(['list'])
