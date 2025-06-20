import unittest
import os
import sys

def run_all_tests():
    # Get the directory containing this script
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return 0 if successful, 1 if there were failures
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
