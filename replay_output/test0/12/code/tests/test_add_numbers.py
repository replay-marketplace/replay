import unittest
import sys
import os

# Add the parent directory to the path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from python_single_file import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(1, 2), 3)
        self.assertEqual(add_numbers(10, 20), 30)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-1, -2), -3)
        self.assertEqual(add_numbers(-10, -20), -30)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-1, 2), 1)
        self.assertEqual(add_numbers(10, -20), -10)
        
    def test_add_zeros(self):
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(0, 10), 10)
        self.assertEqual(add_numbers(-10, 0), -10)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3, places=1)

if __name__ == '__main__':
    unittest.main()