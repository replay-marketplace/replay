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
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 0), 0)
    
    def test_add_floats(self):
        self.assertEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertEqual(add_numbers(-1.5, 1.5), 0.0)
    
    def test_add_mixed(self):
        self.assertEqual(add_numbers(1, 2.5), 3.5)

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddNumbers)
    result = unittest.TextTestRunner().run(suite)
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
