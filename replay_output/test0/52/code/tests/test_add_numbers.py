import sys
import unittest
import os

# Add parent directory to path to import from python_single_file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_single_file import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(5, 3), 8)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-5, 10), 5)
        
    def test_add_zero(self):
        self.assertEqual(add_numbers(7, 0), 7)
        self.assertEqual(add_numbers(0, 0), 0)
        
    def test_add_float_numbers(self):
        self.assertAlmostEqual(add_numbers(3.5, 2.5), 6.0)
        self.assertAlmostEqual(add_numbers(1.1, 2.2), 3.3, places=1)

if __name__ == '__main__':
    unittest.main()