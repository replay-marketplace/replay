import unittest
import sys
import os
from unittest.mock import patch
from io import StringIO

# Add parent directory to path to import add_numbers module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import add_numbers

class TestIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['10', '20'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_valid_input(self, mock_stdout, mock_input):
        add_numbers.main()
        self.assertIn('The sum of 10.0 and 20.0 is 30.0', mock_stdout.getvalue())
    
    @patch('builtins.input', side_effect=['abc', '20'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_invalid_input(self, mock_stdout, mock_input):
        add_numbers.main()
        self.assertIn('Error: Please enter valid numbers', mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()