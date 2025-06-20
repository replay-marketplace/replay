import sys
import os
import unittest
from unittest.mock import patch
import io

# Add the parent directory to sys.path to import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import python_single_file

class TestMainFunction(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '10'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_valid_input(self, mock_stdout, mock_input):
        python_single_file.main()
        self.assertIn('The sum of 5.0 and 10.0 is: 15.0', mock_stdout.getvalue())
        
    @patch('builtins.input', side_effect=['abc', '10'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_invalid_input(self, mock_stdout, mock_input):
        python_single_file.main()
        self.assertIn('Error: Please enter valid numbers', mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()