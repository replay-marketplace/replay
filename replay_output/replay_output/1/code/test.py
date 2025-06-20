'''

This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
work PASSED or FAILED into ../replay/run_pass_fail.txt

'''

import os
import unittest
import sys

def run_tests():
    # Get the directory of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(current_dir, 'tests')
    
    # Add the tests directory to the path
    sys.path.append(tests_dir)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return True if all tests passed, False otherwise
    return result.wasSuccessful()

if __name__ == "__main__":
    passed = run_tests()

    # Ensure directory exists
    os.makedirs(os.path.dirname("../replay/run_tests_pass_fail.txt"), exist_ok=True)
    
    if passed:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("True")
    else:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("False")
