'''

This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
work PASSED or FAILED into ../replay/run_pass_fail.txt

'''

import os
import unittest
import sys
from tests.test_add import TestAddNumbers

def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests to the suite
    suite.addTest(loader.loadTestsFromTestCase(TestAddNumbers))
    
    # Run the tests with a text test runner
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return True if all tests passed, False otherwise
    return result.wasSuccessful()

if __name__ == "__main__":
    passed = run_tests()

    # Ensure directory exists
    os.makedirs("../replay", exist_ok=True)
    
    if passed:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("True")
    else:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("False")
