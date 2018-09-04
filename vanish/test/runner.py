import unittest
from . import test_model


if __name__ == "__main__":
    loader = unittest.TestLoader()

    suites = [
        loader.loadTestsFromModule(test_model)
        ]

    all_tests = unittest.TestSuite(suites)

    unittest.TextTestRunner(verbosity=2).run(all_tests)
