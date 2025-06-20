import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    
    def test_add_integers(self):
        """Test adding two integers"""
        self.assertEqual(add_numbers(1, 2), 3)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(-5, -7), -12)
    
    def test_add_floats(self):
        """Test adding two floating point numbers"""
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3, places=1)
    
    def test_add_mixed_types(self):
        """Test adding an integer and a float"""
        self.assertEqual(add_numbers(1, 2.5), 3.5)
        self.assertEqual(add_numbers(-1, 2.5), 1.5)

if __name__ == '__main__':
    unittest.main()
