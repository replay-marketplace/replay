import sys
import os
import unittest
from unittest.mock import patch
import io

# Add the parent directory to the path so we can import the main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import python_single_file

class TestIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '7'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_valid_input(self, mock_stdout, mock_input):
        python_single_file.main()
        output = mock_stdout.getvalue()
        self.assertIn('Welcome to the addition calculator!', output)
        self.assertIn('The sum of 5.0 and 7.0 is 12.0', output)
        
    @patch('builtins.input', side_effect=['abc', '7'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_invalid_first_input(self, mock_stdout, mock_input):
        python_single_file.main()
        output = mock_stdout.getvalue()
        self.assertIn('Error: Please enter valid numbers.', output)
        
    @patch('builtins.input', side_effect=['5', 'xyz'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_invalid_second_input(self, mock_stdout, mock_input):
        python_single_file.main()
        output = mock_stdout.getvalue()
        self.assertIn('Error: Please enter valid numbers.', output)

if __name__ == '__main__':
    unittest.main()