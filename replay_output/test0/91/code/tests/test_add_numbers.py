import unittest
import sys
import os

# Add the parent directory to the path so we can import the add_numbers module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(1, 2), 3)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-1, -2), -3)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-1, 2), 1)
        
    def test_add_zero(self):
        self.assertEqual(add_numbers(5, 0), 5)
        self.assertEqual(add_numbers(0, 5), 5)
        
    def test_add_float_numbers(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)

if __name__ == "__main__":
    unittest.main()
