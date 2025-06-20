import sys
import os
import unittest

# Add parent directory to path to import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_single_file import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
    
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)
    
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-2, 5), 3)
    
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(2.5, 3.5), 6.0)

if __name__ == '__main__':
    unittest.main()