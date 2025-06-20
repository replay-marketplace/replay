import unittest
import sys
import os

# Add parent directory to path to import the adder module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adder import add_numbers

class TestAdder(unittest.TestCase):
    def test_add_integers(self):
        # Due to the intentional bug, this should fail
        self.assertEqual(add_numbers(2, 3), 5)  # Expected 5, but will get 6
        
    def test_add_floats(self):
        # Due to the intentional bug, this should fail
        self.assertAlmostEqual(add_numbers(2.5, 3.5), 6.0)  # Expected 6.0, but will get 7.0
        
    def test_add_negative(self):
        # Due to the intentional bug, this should fail
        self.assertEqual(add_numbers(-1, -1), -2)  # Expected -2, but will get -1

if __name__ == "__main__":
    unittest.main()
