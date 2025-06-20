'''
This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
word PASSED or FAILED into ../replay/run_pass_fail.txt
'''

import unittest
import os
from add_numbers import add_numbers


class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(5, 3), 8)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-5, -3), -8)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-5, 8), 3)
        
    def test_add_zeros(self):
        self.assertEqual(add_numbers(0, 0), 0)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAddNumbers)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    # Ensure the replay directory exists
    os.makedirs("../replay", exist_ok=True)
    
    passed = run_tests()

    # Write PASSED or FAILED as specified in the comments
    with open("../replay/run_pass_fail.txt", "w") as f:
        f.write("PASSED" if passed else "FAILED")
