import unittest
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(1, 2), 3)
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(-5, -7), -12)
    
    def test_add_floats(self):
        self.assertEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3)
        
    def test_add_large_numbers(self):
        self.assertEqual(add_numbers(1000000, 2000000), 3000000)
        
    def test_add_negative_and_positive(self):
        self.assertEqual(add_numbers(-10, 15), 5)

if __name__ == "__main__":
    unittest.main()