import sys
import os
import unittest
from unittest.mock import patch
from io import StringIO

# Add parent directory to path to import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_single_file import main

class TestMain(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '7'])
    def test_main_valid_input(self, mock_input):
        # Redirect stdout to capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        main()
        
        # Reset redirect
        sys.stdout = sys.__stdout__
        
        # Check if output contains expected results
        self.assertIn('The sum of 5.0 and 7.0 is 12.0', captured_output.getvalue())
    
    @patch('builtins.input', side_effect=['abc', '7'])
    def test_main_invalid_input(self, mock_input):
        # Redirect stdout to capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        main()
        
        # Reset redirect
        sys.stdout = sys.__stdout__
        
        # Check if error message is displayed
        self.assertIn('Error: Please enter valid numbers', captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()