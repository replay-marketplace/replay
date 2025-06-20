import unittest
import sys
import os

# Add parent directory to path so we can import add_numbers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    
    def test_add_integers(self):
        self.assertEqual(add_numbers(1, 2), 3)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(-1, -1), -2)
    
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(-1.5, 1.5), 0.0)
    
    def test_add_mixed(self):
        self.assertAlmostEqual(add_numbers(1, 2.5), 3.5)
        
    def test_add_large_numbers(self):
        self.assertEqual(add_numbers(1000000, 2000000), 3000000)
        
    def test_add_zero(self):
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(42, 0), 42)
        self.assertEqual(add_numbers(0, 42), 42)

if __name__ == "__main__":
    unittest.main()