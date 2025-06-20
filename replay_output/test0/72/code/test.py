'''

This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
work PASSED or FAILED into ../replay/run_pass_fail.txt

'''

import os
import unittest
import sys
from tests.test_calculator import TestCalculator

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCalculator)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    passed = run_tests()

    os.makedirs("../replay", exist_ok=True)
    if passed:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("True")
    else:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("False")
