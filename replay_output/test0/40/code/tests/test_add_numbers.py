import unittest
import sys
import os

# Add the parent directory to the system path to import the add_numbers module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(5, 3), 8)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-5, -3), -8)
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-5, 8), 3)
        
    def test_add_zero(self):
        self.assertEqual(add_numbers(5, 0), 5)
        self.assertEqual(add_numbers(0, 5), 5)
        self.assertEqual(add_numbers(0, 0), 0)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(3.5, 2.5), 6.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3, places=1)

if __name__ == '__main__':
    unittest.main()
