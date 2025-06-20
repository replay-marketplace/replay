import unittest
import sys
import os

# Add parent directory to path to import add_numbers module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(5, 3), 8)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 0), 0)
    
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(2.5, 3.5), 6.0)
        self.assertAlmostEqual(add_numbers(-1.5, 0.5), -1.0)
    
    def test_add_mixed(self):
        self.assertEqual(add_numbers(5, 3.5), 8.5)
    
    def test_add_large_numbers(self):
        self.assertEqual(add_numbers(1000000, 2000000), 3000000)
    
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-50, -25), -75)

if __name__ == "__main__":
    unittest.main()