import unittest
from unittest.mock import patch
import io
import sys
import os

# Add the parent directory to the system path to import the add_numbers module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import add_numbers

class TestInputHandling(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '3'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_input(self, mock_stdout, mock_input):
        add_numbers.main()
        self.assertEqual(mock_stdout.getvalue(), 'The sum of 5.0 and 3.0 is: 8.0\n')
        
    @patch('builtins.input', side_effect=['abc', '3'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_input(self, mock_stdout, mock_input):
        add_numbers.main()
        self.assertEqual(mock_stdout.getvalue(), 'Error: Please enter valid numbers.\n')

if __name__ == '__main__':
    unittest.main()
