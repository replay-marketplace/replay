import sys
import os
import unittest

# Add parent directory to path to import calculator module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import add_numbers

class TestCalculator(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(5, 3), 8)
        self.assertEqual(add_numbers(-5, 3), -2)
        self.assertEqual(add_numbers(0, 0), 0)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(2.5, 3.5), 6.0)
        self.assertAlmostEqual(add_numbers(-1.5, 1.5), 0.0)
        
    def test_add_mixed_types(self):
        self.assertEqual(add_numbers(5, 3.5), 8.5)
        self.assertEqual(add_numbers(-2.5, 5), 2.5)

if __name__ == '__main__':
    unittest.main()
