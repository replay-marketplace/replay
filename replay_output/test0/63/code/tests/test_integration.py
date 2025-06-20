import unittest
import sys
import os
import io
from unittest.mock import patch

# Add parent directory to path so we can import add_numbers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import add_numbers

class TestAddNumbersIntegration(unittest.TestCase):
    
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['5', '7'])
    def test_main_function_with_valid_input(self, mock_input, mock_stdout):
        add_numbers.main()
        output = mock_stdout.getvalue()
        self.assertIn('Program to add two numbers', output)
        self.assertIn('The sum of 5.0 and 7.0 is 12.0', output)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['abc', '7'])
    def test_main_function_with_invalid_input(self, mock_input, mock_stdout):
        add_numbers.main()
        output = mock_stdout.getvalue()
        self.assertIn('Error: Please enter valid numbers', output)

if __name__ == "__main__":
    unittest.main()