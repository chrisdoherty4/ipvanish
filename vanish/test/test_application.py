import unittest
import sys
from .. import application
from cStringIO import StringIO


class TestCommands(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sys_stdout = sys.stdout
        cls.sys_stderr = sys.stderr

        sys.stdout = cls.stdout = StringIO()
        sys.stderr = cls.stderr = StringIO()

    @classmethod
    def tearDownClass(cls):
        sys.stdout = cls.sys_stdout
        sys.stderr = cls.sys_stderr

    def test_invalidCommand(self):
        app = application.Vanish()

        with self.assertRaises(SystemExit):
            app.run(['invalid-command'])

    def test_incompleteSync(self):
        app = application.Vanish()

        with self.assertRaises(SystemExit):
            app.run(['sync'])

    def test_incompleteList(self):
        app = application.Vanish()

        with self.assertRaises(SystemExit):
            app.run(['list'])
