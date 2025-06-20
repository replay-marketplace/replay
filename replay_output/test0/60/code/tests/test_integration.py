import unittest
import sys
import os
from unittest.mock import patch
import io

# Add parent directory to path so we can import add_numbers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import add_numbers

class TestIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '10'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_valid_input(self, mock_stdout, mock_input):
        add_numbers.main()
        self.assertIn('The sum of 5.0 and 10.0 is: 15.0', mock_stdout.getvalue())
        
    @patch('builtins.input', side_effect=['abc', '10'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_invalid_input(self, mock_stdout, mock_input):
        add_numbers.main()
        self.assertIn('Error: Please enter valid numbers', mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()