#!/usr/bin/env python3

import unittest
import sys
import os

# Add parent directory to path to import add_numbers module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        self.assertEqual(add_numbers(2, 3), 5)
        
    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        self.assertEqual(add_numbers(-2, -3), -5)
        
    def test_add_mixed_numbers(self):
        """Test adding a positive and negative number."""
        self.assertEqual(add_numbers(2, -3), -1)
        
    def test_add_zero(self):
        """Test adding zero to a number."""
        self.assertEqual(add_numbers(5, 0), 5)
        self.assertEqual(add_numbers(0, 5), 5)
        
    def test_add_float_numbers(self):
        """Test adding floating point numbers."""
        self.assertAlmostEqual(add_numbers(2.5, 3.5), 6.0)

if __name__ == "__main__":
    unittest.main()
