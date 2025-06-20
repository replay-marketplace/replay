import unittest
import os

def run_tests():
    # Discover and run all tests in the 'tests' directory
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result

if __name__ == '__main__':
    result = run_tests()
    # Exit with non-zero code if tests failed
    if not result.wasSuccessful():
        exit(1)