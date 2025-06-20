import unittest
import sys
import os

# Add parent directory to path to import calculator module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import add_numbers

class TestCalculator(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(1, 2), 3)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(-5, -7), -12)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3, places=1)
        
    def test_add_mixed(self):
        self.assertEqual(add_numbers(1, 2.5), 3.5)
        
    def test_add_zero(self):
        self.assertEqual(add_numbers(5, 0), 5)
        self.assertEqual(add_numbers(0, 0), 0)

if __name__ == "__main__":
    unittest.main()
