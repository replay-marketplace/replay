'''
This is the main test file where all the tests should go.

The key thing is to check if all the tests passed or failed and then to write the
word PASSED or FAILED into ../replay/run_pass_fail.txt
'''

import unittest
from add import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(5, 3), 8)
    
    def test_add_floats(self):
        self.assertEqual(add_numbers(2.5, 3.5), 6.0)
    
    def test_add_negative(self):
        self.assertEqual(add_numbers(-1, -2), -3)
    
    def test_add_mixed(self):
        self.assertEqual(add_numbers(-1, 5), 4)

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAddNumbers)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    passed = run_tests()

    if passed:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("True")
    else:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("False")