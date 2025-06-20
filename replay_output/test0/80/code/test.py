'''

This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
work PASSED or FAILED into ../replay/run_pass_fail.txt

'''

import os
import unittest
import sys

def run_tests():
    test_loader = unittest.TestLoader()
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    test_suite = test_loader.discover(test_dir, pattern='test_*.py')
    
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    passed = run_tests()

    if passed:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("True")
    else:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("False")
