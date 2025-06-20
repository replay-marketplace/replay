import sys
import os
import unittest
from unittest.mock import patch
import io

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import python_single_file

class TestInputValidation(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '3'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_input(self, mock_stdout, mock_input):
        python_single_file.main()
        self.assertIn('The sum of 5.0 and 3.0 is 8.0', mock_stdout.getvalue())
    
    @patch('builtins.input', side_effect=['abc', '3'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_first_input(self, mock_stdout, mock_input):
        python_single_file.main()
        self.assertIn('Error: Please enter valid numbers', mock_stdout.getvalue())
    
    @patch('builtins.input', side_effect=['5', 'xyz'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_second_input(self, mock_stdout, mock_input):
        python_single_file.main()
        self.assertIn('Error: Please enter valid numbers', mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()