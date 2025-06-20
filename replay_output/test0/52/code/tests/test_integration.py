import sys
import unittest
import os
from unittest.mock import patch
import io

# Add parent directory to path to import from python_single_file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import python_single_file

class TestIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '7'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_function(self, mock_stdout, mock_input):
        python_single_file.main()
        output = mock_stdout.getvalue()
        self.assertIn('Welcome to the number adder program!', output)
        self.assertIn('The sum of 5.0 and 7.0 is: 12.0', output)
    
    @patch('builtins.input', side_effect=['invalid', '5', 'invalid', '7'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_invalid_input(self, mock_stdout, mock_input):
        python_single_file.main()
        output = mock_stdout.getvalue()
        self.assertIn('Invalid input. Please enter a number.', output)
        self.assertIn('The sum of 5.0 and 7.0 is: 12.0', output)

if __name__ == '__main__':
    unittest.main()