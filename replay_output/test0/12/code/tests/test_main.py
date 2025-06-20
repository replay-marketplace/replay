import unittest
from unittest.mock import patch
import io
import sys
import os

# Add the parent directory to the path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import python_single_file

class TestMain(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '7'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_valid_input(self, mock_stdout, mock_input):
        python_single_file.main()
        expected_output = "This program adds two numbers together.\nThe sum of 5.0 and 7.0 is 12.0\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)
    
    @patch('builtins.input', side_effect=['abc', '7'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_invalid_input(self, mock_stdout, mock_input):
        python_single_file.main()
        expected_output = "This program adds two numbers together.\nError: Please enter valid numbers.\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()