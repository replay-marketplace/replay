import sys
import os
import unittest

# Add the parent directory to the path so we can import the main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_single_file import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(5, 3), 8)
        self.assertEqual(add_numbers(10, 20), 30)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-5, -3), -8)
        self.assertEqual(add_numbers(-10, -20), -30)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-5, 10), 5)
        self.assertEqual(add_numbers(10, -20), -10)
        
    def test_add_zeros(self):
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(10, 0), 10)
        self.assertEqual(add_numbers(0, 10), 10)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3, places=1)

if __name__ == '__main__':
    unittest.main()