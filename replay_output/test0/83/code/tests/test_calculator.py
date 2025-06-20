import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calculator import add_numbers


class TestCalculator(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-2, 5), 3)
        
    def test_add_zeros(self):
        self.assertEqual(add_numbers(0, 0), 0)
        
    def test_add_decimal_numbers(self):
        self.assertEqual(add_numbers(1.5, 2.5), 4.0)


if __name__ == "__main__":
    unittest.main()