import unittest
import os

def run_tests():
    # Discover and run all tests in the tests directory
    test_loader = unittest.TestLoader()
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_suite = test_loader.discover(test_dir, pattern="test_*.py")
    
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    return result

if __name__ == "__main__":
    run_tests()
