'''
This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
word PASSED or FAILED into ../replay/run_pass_fail.txt
'''

import unittest
from add_numbers import add_numbers
import os


class TestAddNumbers(unittest.TestCase):
    
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(5, 3), 8)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-5, -3), -8)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-5, 8), 3)
        
    def test_add_zero(self):
        self.assertEqual(add_numbers(10, 0), 10)
        
    def test_add_float_numbers(self):
        self.assertAlmostEqual(add_numbers(2.5, 3.5), 6.0)


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAddNumbers)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    passed = run_tests()

    # Ensure the directory exists
    os.makedirs("../replay", exist_ok=True)
    
    if passed:
        with open("../replay/run_pass_fail.txt", "w") as f:
            f.write("PASSED")
    else:
        with open("../replay/run_pass_fail.txt", "w") as f:
            f.write("FAILED")
