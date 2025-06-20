import unittest
import sys
import os

# Add parent directory to path to import add_numbers module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(1, 2), 3)
        self.assertEqual(add_numbers(100, 200), 300)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-1, -2), -3)
        self.assertEqual(add_numbers(-10, -20), -30)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-1, 5), 4)
        self.assertEqual(add_numbers(10, -5), 5)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3, places=1)
        
    def test_add_zeros(self):
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(0, 10), 10)
        self.assertEqual(add_numbers(-5, 0), -5)

if __name__ == "__main__":
    unittest.main()