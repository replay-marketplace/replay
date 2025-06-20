import unittest
import sys
import os

# Add parent directory to path to import calculator module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import add_numbers

class TestCalculator(unittest.TestCase):
    def test_add_two_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        
    def test_add_positive_and_negative_numbers(self):
        self.assertEqual(add_numbers(5, -3), 2)
        
    def test_add_two_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)
        
    def test_add_float_numbers(self):
        self.assertAlmostEqual(add_numbers(2.5, 3.5), 6.0)
        
    def test_add_zero(self):
        self.assertEqual(add_numbers(5, 0), 5)
        self.assertEqual(add_numbers(0, 0), 0)

if __name__ == "__main__":
    unittest.main()
