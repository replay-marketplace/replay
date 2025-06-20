import unittest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import add_numbers


class TestAddNumbersIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '7'])
    @patch('builtins.print')
    def test_main_valid_input(self, mock_print, mock_input):
        add_numbers.main()
        mock_print.assert_called_with('The sum of 5.0 and 7.0 is 12.0')
        
    @patch('builtins.input', side_effect=['abc', '7'])
    @patch('builtins.print')
    def test_main_invalid_input(self, mock_print, mock_input):
        add_numbers.main()
        mock_print.assert_called_with('Error: Please enter valid numbers.')


if __name__ == '__main__':
    unittest.main()
