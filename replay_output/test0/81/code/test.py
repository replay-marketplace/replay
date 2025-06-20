'''

This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
work PASSED or FAILED into ../replay/run_pass_fail.txt

'''

import os
import unittest
import sys

def run_tests():
    # Import the test module
    from tests.test_adder import TestAdder
    
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add all tests from TestAdder
    test_suite.addTest(unittest.makeSuite(TestAdder))
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)
    
    # Return True if all tests passed, False otherwise
    return test_result.wasSuccessful()

if __name__ == "__main__":
    passed = run_tests()

    if passed:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("True")
    else:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("False")
