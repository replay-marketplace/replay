import unittest
import sys
import os

# Add parent directory to path so we can import add_numbers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from add_numbers import add_numbers

class TestEdgeCases(unittest.TestCase):
    
    def test_large_numbers(self):
        self.assertEqual(add_numbers(1000000, 1000000), 2000000)
        
    def test_small_decimals(self):
        self.assertAlmostEqual(add_numbers(0.000001, 0.000001), 0.000002)
        
    def test_mixed_types(self):
        # Python handles type conversion automatically
        self.assertEqual(add_numbers(int(1), float(2.0)), 3.0)
        
    def test_zero_cases(self):
        self.assertEqual(add_numbers(0, 5), 5)
        self.assertEqual(add_numbers(5, 0), 5)

if __name__ == "__main__":
    unittest.main()