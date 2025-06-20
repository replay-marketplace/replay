import sys
import os
import unittest
from unittest.mock import patch
from io import StringIO

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import add_numbers

class TestIntegration(unittest.TestCase):
    def test_main_hardcoded_values(self):
        # Capture stdout
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Mock the input to exit after the hardcoded example
            with patch('builtins.input', side_effect=['']):
                try:
                    add_numbers.main()
                except EOFError:
                    pass  # This is expected when input is exhausted
                
                output = fake_out.getvalue()
                self.assertIn("Sum of 1, 2, 3, 4, 5 = 15", output)
    
    def test_main_user_input(self):
        # Test with user input
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', return_value="10 20 30"):
                add_numbers.main()
                
                output = fake_out.getvalue()
                self.assertIn("Sum of 10.0, 20.0, 30.0 = 60.0", output)
    
    def test_main_invalid_input(self):
        # Test with invalid input
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', return_value="10 abc 30"):
                add_numbers.main()
                
                output = fake_out.getvalue()
                self.assertIn("Error: Please enter valid numbers", output)

if __name__ == '__main__':
    unittest.main()
