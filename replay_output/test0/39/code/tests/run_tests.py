import unittest
import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Discover and run all tests
if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.dirname(__file__), pattern='test_*.py')
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
