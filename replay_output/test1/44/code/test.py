'''
This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
work PASSED or FAILED into ../replay/run_pass_fail.txt
'''

import os
import unittest
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(5, 3), 8)  # Now passes with the fix
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-5, -3), -8)  # Now passes with the fix
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-5, 8), 3)  # Now passes with the fix

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddNumbers)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return len(result.errors) == 0 and len(result.failures) == 0

if __name__ == "__main__":
    passed = run_tests()

    # Create directory if it doesn't exist
    os.makedirs("../replay", exist_ok=True)
    
    if passed:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("PASSED")
    else:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("FAILED")
