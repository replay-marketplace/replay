import sys
import os
import unittest
from unittest.mock import patch
import io

# Add the parent directory to the path so we can import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import python_single_file

class TestMainFunction(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '7'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_valid_input(self, mock_stdout, mock_input):
        python_single_file.main()
        self.assertIn("The sum of 5.0 and 7.0 is 12.0", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['invalid', '7'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_invalid_input(self, mock_stdout, mock_input):
        python_single_file.main()
        self.assertIn("Error: Please enter valid numbers.", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()