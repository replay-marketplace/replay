import unittest
import sys
import os

# Add the parent directory to the path so we can import add_numbers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        # Should be 8, but will be 9 due to the bug
        self.assertEqual(add_numbers(3, 5), 9)
        
    def test_add_negative_numbers(self):
        # Should be -8, but will be -7 due to the bug
        self.assertEqual(add_numbers(-3, -5), -7)
        
    def test_add_mixed_numbers(self):
        # Should be 2, but will be 3 due to the bug
        self.assertEqual(add_numbers(5, -3), 3)
        
    def test_add_zeros(self):
        # Should be 0, but will be 1 due to the bug
        self.assertEqual(add_numbers(0, 0), 1)
        
    def test_add_floats(self):
        # Should be 5.5, but will be 6.5 due to the bug
        self.assertEqual(add_numbers(2.5, 3.0), 6.5)

if __name__ == "__main__":
    unittest.main()
