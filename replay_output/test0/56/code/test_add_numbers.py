import unittest
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(5, 3), 8)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 0), 0)
    
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(2.5, 3.5), 6.0)
        self.assertAlmostEqual(add_numbers(-1.5, 0.5), -1.0)
    
    def test_add_mixed(self):
        self.assertEqual(add_numbers(5, 3.5), 8.5)

if __name__ == "__main__":
    unittest.main()
