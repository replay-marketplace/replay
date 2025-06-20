import unittest
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from add_numbers import add_numbers


class TestAddNumbers(unittest.TestCase):
    
    def test_add_integers(self):
        self.assertEqual(add_numbers(1, 2), 3)
        self.assertEqual(add_numbers(-1, 2), 1)
        self.assertEqual(add_numbers(-1, -2), -3)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(-1.5, 2.5), 1.0)
        
    def test_add_zero(self):
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(5, 0), 5)
        
    def test_add_large_numbers(self):
        self.assertEqual(add_numbers(10000000, 20000000), 30000000)


if __name__ == '__main__':
    unittest.main()
