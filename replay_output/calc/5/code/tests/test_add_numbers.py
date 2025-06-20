import unittest
import sys
import os

# Add the parent directory to the path so we can import the add_numbers module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(1, 2, 3), 6)
        self.assertEqual(add_numbers(10, 20, 30, 40, 50), 150)
    
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-1, -2, -3), -6)
        self.assertEqual(add_numbers(-10, -20), -30)
    
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(1, -1), 0)
        self.assertEqual(add_numbers(10, -5, 3, -8), 0)
    
    def test_add_floating_point_numbers(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2, 0.3), 0.6, places=10)
    
    def test_add_no_numbers(self):
        self.assertEqual(add_numbers(), 0)
    
    def test_add_single_number(self):
        self.assertEqual(add_numbers(5), 5)
        self.assertEqual(add_numbers(-3), -3)

if __name__ == '__main__':
    unittest.main()
