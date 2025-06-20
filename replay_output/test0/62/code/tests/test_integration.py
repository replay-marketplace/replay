import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch

# Add parent directory to sys.path to import add_numbers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import add_numbers

class TestIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '7'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_valid_input(self, mock_stdout, mock_input):
        add_numbers.main()
        expected_output = "The sum of 5.0 and 7.0 is 12.0\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)
    
    @patch('builtins.input', side_effect=['abc', '7'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_invalid_input(self, mock_stdout, mock_input):
        add_numbers.main()
        expected_output = "Error: Please enter valid numbers.\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()
