import sys
import os
import unittest

# Add the parent directory to sys.path to import the main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_single_file import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(100, 50), 150)
    
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)
        self.assertEqual(add_numbers(-10, -20), -30)
    
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-5, 10), 5)
        self.assertEqual(add_numbers(8, -3), 5)
    
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3, places=1)
    
    def test_add_zero(self):
        self.assertEqual(add_numbers(0, 5), 5)
        self.assertEqual(add_numbers(10, 0), 10)
        self.assertEqual(add_numbers(0, 0), 0)

if __name__ == "__main__":
    unittest.main()