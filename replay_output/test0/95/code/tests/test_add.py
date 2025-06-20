import unittest
import sys
import os

# Add parent directory to path to import add.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from add import add_numbers


class TestAddNumbers(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add_numbers(1, 2), 3)
        self.assertEqual(add_numbers(10, 20), 30)
    
    def test_negative_numbers(self):
        self.assertEqual(add_numbers(-1, -1), -2)
        self.assertEqual(add_numbers(-5, -7), -12)
    
    def test_mixed_numbers(self):
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(5, -3), 2)
    
    def test_zero(self):
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(0, 10), 10)
        self.assertEqual(add_numbers(-5, 0), -5)
    
    def test_float_numbers(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3, places=1)


if __name__ == "__main__":
    unittest.main()
