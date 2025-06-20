'''
This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
word PASSED or FAILED into ../replay/run_pass_fail.txt
'''

import os
import unittest
from calculator import add_numbers


class TestCalculator(unittest.TestCase):
    """
    Test cases for the calculator functionality.
    """
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        self.assertEqual(add_numbers(5, 3), 8)
    
    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        self.assertEqual(add_numbers(-5, -3), -8)
    
    def test_add_mixed_numbers(self):
        """Test adding a positive and negative number."""
        self.assertEqual(add_numbers(5, -3), 2)
    
    def test_add_zeros(self):
        """Test adding zeros."""
        self.assertEqual(add_numbers(0, 0), 0)
    
    def test_add_floats(self):
        """Test adding floating point numbers."""
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)


def run_tests():
    """Run all tests and return True if all tests pass, False otherwise."""
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return test_result.wasSuccessful()


if __name__ == "__main__":
    passed = run_tests()

    if passed:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("True")
    else:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("False")