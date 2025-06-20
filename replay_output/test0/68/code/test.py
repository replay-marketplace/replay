'''
This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
work PASSED or FAILED into ../replay/run_pass_fail.txt
'''

import os
import unittest
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(1, 2), 3)
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(-5, -7), -12)
    
    def test_add_floats(self):
        self.assertEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertEqual(add_numbers(0.1, 0.2), 0.3)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3)

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAddNumbers)
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
