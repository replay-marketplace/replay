import unittest
import sys
import os

# Add parent directory to path so we can import calculator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import add_numbers

class TestCalculator(unittest.TestCase):
    
    def test_add_positive_numbers(self):
        # This test should fail because of the bug
        self.assertEqual(add_numbers(2, 3), 5)
    
    def test_add_negative_numbers(self):
        # This test should fail because of the bug
        self.assertEqual(add_numbers(-2, -3), -5)
    
    def test_add_mixed_numbers(self):
        # This test should fail because of the bug
        self.assertEqual(add_numbers(-2, 5), 3)
    
    def test_add_zero(self):
        # This test should fail because of the bug
        self.assertEqual(add_numbers(0, 0), 0)

if __name__ == "__main__":
    unittest.main()
