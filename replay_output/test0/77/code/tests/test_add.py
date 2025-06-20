import unittest
import sys
import os

# Add parent directory to path so we can import add.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from add import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(1, 2), 3)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-1, -2), -3)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-1, 2), 1)
        
    def test_add_float_numbers(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)

if __name__ == "__main__":
    unittest.main()
