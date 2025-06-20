import unittest
import sys
import os

# Add the parent directory to the path so we can import the adder module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adder import add_two_numbers

class TestAdder(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_two_numbers(2, 3), 6)  # Should fail: 2+3=5, but function returns 6
        
    def test_add_negative_numbers(self):
        self.assertEqual(add_two_numbers(-2, -3), -4)  # Should fail: -2+(-3)=-5, but function returns -4
        
    def test_add_mixed_numbers(self):
        self.assertEqual(add_two_numbers(5, -3), 3)  # Should fail: 5+(-3)=2, but function returns 3
        
    def test_add_zeros(self):
        self.assertEqual(add_two_numbers(0, 0), 1)  # Should fail: 0+0=0, but function returns 1

if __name__ == "__main__":
    unittest.main()
