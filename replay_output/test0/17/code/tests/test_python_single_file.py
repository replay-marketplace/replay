import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_single_file import add_numbers

class TestAddNumbers(unittest.TestCase):
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers"""
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(10, 5), 15)
    
    def test_add_negative_numbers(self):
        """Test adding two negative numbers"""
        self.assertEqual(add_numbers(-2, -3), -5)
        self.assertEqual(add_numbers(-10, -5), -15)
    
    def test_add_mixed_numbers(self):
        """Test adding a positive and a negative number"""
        self.assertEqual(add_numbers(2, -3), -1)
        self.assertEqual(add_numbers(-10, 5), -5)
    
    def test_add_zeros(self):
        """Test adding zeros"""
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(10, 0), 10)
        self.assertEqual(add_numbers(0, 10), 10)
    
    def test_add_floats(self):
        """Test adding floating point numbers"""
        self.assertAlmostEqual(add_numbers(2.5, 3.5), 6.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3, places=1)

if __name__ == '__main__':
    unittest.main()