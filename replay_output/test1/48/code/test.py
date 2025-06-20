'''
This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
word PASSED or FAILED into ../replay/run_pass_fail.txt
'''

import os
import unittest
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
    
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)
    
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-2, 5), 3)

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddNumbers)
    result = unittest.TextTestRunner().run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    passed = run_tests()

    os.makedirs("../replay", exist_ok=True)
    if passed:
        with open("../replay/run_pass_fail.txt", "w") as f:
            f.write("PASSED")
    else:
        with open("../replay/run_pass_fail.txt", "w") as f:
            f.write("FAILED")