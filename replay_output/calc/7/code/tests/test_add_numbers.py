import sys
import os
import unittest

# Add the parent directory to the path so we can import add_numbers
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add_numbers(1, 2, 3, 4, 5), 15)
        self.assertEqual(add_numbers(10, 20), 30)
    
    def test_negative_numbers(self):
        self.assertEqual(add_numbers(-1, -2, -3), -6)
        self.assertEqual(add_numbers(-5, 5), 0)
    
    def test_floating_point_numbers(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2, 0.3), 0.6)
    
    def test_empty_args(self):
        self.assertEqual(add_numbers(), 0)
    
    def test_single_arg(self):
        self.assertEqual(add_numbers(5), 5)

if __name__ == '__main__':
    unittest.main()
