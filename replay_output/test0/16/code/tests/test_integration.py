import sys
import os
import unittest
from unittest.mock import patch
from io import StringIO

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import python_single_file

class TestIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '3'])
    def test_main_valid_input(self, mock_input):
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Run the main function
        python_single_file.main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check the output
        self.assertIn('The sum of 5.0 and 3.0 is 8.0', captured_output.getvalue())
    
    @patch('builtins.input', side_effect=['abc', '3'])
    def test_main_invalid_input(self, mock_input):
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Run the main function
        python_single_file.main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check the output
        self.assertIn('Error: Please enter valid numbers', captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()