import unittest
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(3, 5), 8)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-5, 10), 5)
        
    def test_add_zero(self):
        self.assertEqual(add_numbers(7, 0), 7)
        self.assertEqual(add_numbers(0, 0), 0)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(3.5, 2.1), 5.6)
        
    def test_add_large_numbers(self):
        self.assertEqual(add_numbers(1000000, 2000000), 3000000)

if __name__ == '__main__':
    unittest.main()
