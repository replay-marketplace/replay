import os
import unittest
import sys

def run_all_tests():
    # Create test suite
    loader = unittest.TestLoader()
    # Find all tests in the tests directory
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return whether all tests passed
    return result.wasSuccessful()

if __name__ == "__main__":
    passed = run_all_tests()
    
    # Create the replay directory if it doesn't exist
    os.makedirs("../replay", exist_ok=True)
    
    # Write the result to the file
    with open("../replay/run_tests_pass_fail.txt", "w") as f:
        f.write(str(passed))
    
    # Exit with appropriate code
    sys.exit(0 if passed else 1)