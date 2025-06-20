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
        self.assertEqual(add_numbers(5, 3), 8)
        self.assertEqual(add_numbers(-5, 3), -2)
        self.assertEqual(add_numbers(0, 0), 0)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(5.5, 3.2), 8.7)
        self.assertAlmostEqual(add_numbers(-5.5, 3.2), -2.3)
        
    def test_add_mixed(self):
        self.assertEqual(add_numbers(5, 3.0), 8.0)
        self.assertEqual(add_numbers(5.0, 3), 8.0)


def run_tests():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAddNumbers)
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    passed = run_tests()
    
    # Create directory if it doesn't exist
    os.makedirs("../replay", exist_ok=True)
    
    if passed:
        with open("../replay/run_pass_fail.txt", "w") as f:
            f.write("PASSED")
    else:
        with open("../replay/run_pass_fail.txt", "w") as f:
            f.write("FAILED")
