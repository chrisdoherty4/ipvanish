import sys
import unittest
from . import test_model
from . import test_application


if __name__ == "__main__":
    loader = unittest.TestLoader()

    suites = [
        loader.loadTestsFromModule(test_model),
        loader.loadTestsFromModule(test_application)
    ]

    all_tests = unittest.TestSuite(suites)

    sys.exit(unittest.TextTestRunner(verbosity=2).run(all_tests).wasSuccessful())
