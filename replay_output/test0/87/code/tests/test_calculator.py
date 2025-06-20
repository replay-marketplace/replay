import unittest
import sys
import os

# Add the parent directory to the path so we can import calculator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import add_numbers

class TestCalculator(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)  # Should be 5, but with bug it's 6
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)  # Should be -5, but with bug it's -4
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(2, -3), -1)  # Should be -1, but with bug it's 0
        
    def test_add_zero(self):
        self.assertEqual(add_numbers(5, 0), 5)  # Should be 5, but with bug it's 6
        
    def test_add_decimals(self):
        self.assertAlmostEqual(add_numbers(2.5, 3.5), 6.0)  # Should be 6.0, but with bug it's 7.0

if __name__ == "__main__":
    unittest.main()
