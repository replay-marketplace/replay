import unittest

def run_tests():
    """Discover and run all tests in the tests directory"""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('.', pattern='test_*.py')
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)

if __name__ == '__main__':
    run_tests()
