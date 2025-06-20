import unittest
import sys
import os
from unittest.mock import patch
from io import StringIO

# Add the parent directory to the path so we can import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import add_numbers

class TestAddNumbersIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '7'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_valid_input(self, mock_stdout, mock_input):
        add_numbers.main()
        self.assertIn('The sum of 5.0 and 7.0 is: 12.0', mock_stdout.getvalue())
    
    @patch('builtins.input', side_effect=['abc', '7'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_invalid_input(self, mock_stdout, mock_input):
        add_numbers.main()
        self.assertIn('Error: Please enter valid numbers', mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()
