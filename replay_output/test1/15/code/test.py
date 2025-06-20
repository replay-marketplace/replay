'''
This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
word PASSED or FAILED into ../replay/run_pass_fail.txt
'''

import os
import unittest
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(5, 7), 12)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(3.5, 2.1), 5.6)
        
    def test_add_negative(self):
        self.assertEqual(add_numbers(-8, 3), -5)
        
    def test_add_zero(self):
        self.assertEqual(add_numbers(10, 0), 10)

def run_tests():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAddNumbers)
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
