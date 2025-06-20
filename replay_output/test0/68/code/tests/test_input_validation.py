import unittest
from unittest.mock import patch
import io
import sys
from add_numbers import main

class TestInputValidation(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '10'])
    def test_valid_input(self, mock_input):
        # Redirect stdout to capture output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Call the main function
        main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check the output
        self.assertIn("The sum of 5.0 and 10.0 is: 15.0", captured_output.getvalue())
    
    @patch('builtins.input', side_effect=['abc', '10'])
    def test_invalid_input(self, mock_input):
        # Redirect stdout to capture output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Call the main function
        main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check the output
        self.assertIn("Error: Please enter valid numbers.", captured_output.getvalue())

if __name__ == "__main__":
    unittest.main()