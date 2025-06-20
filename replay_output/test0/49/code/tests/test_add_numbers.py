import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_single_file import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-2, 5), 3)
        
    def test_add_zeros(self):
        self.assertEqual(add_numbers(0, 0), 0)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(2.5, 3.5), 6.0)

if __name__ == '__main__':
    unittest.main()