import unittest
import sys
import os
from unittest.mock import patch
from io import StringIO

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from add_numbers import main

class TestIntegration(unittest.TestCase):
    
    @patch('builtins.input', side_effect=['5', '3'])
    def test_main_valid_input(self, mock_input):
        # Redirect stdout to capture print statements
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Call the main function
        main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check the output
        output = captured_output.getvalue()
        self.assertIn("The sum of 5.0 and 3.0 is 8.0", output)
    
    @patch('builtins.input', side_effect=['abc', '3'])
    def test_main_invalid_input(self, mock_input):
        # Redirect stdout to capture print statements
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Call the main function
        main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check the output
        output = captured_output.getvalue()
        self.assertIn("Error: Please enter valid numbers", output)

if __name__ == '__main__':
    unittest.main()
