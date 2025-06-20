import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch

# Add parent directory to path so we can import add_numbers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from add_numbers import main

class TestIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '7'])
    def test_main_function(self, mock_input):
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Run the main function
        main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check the output
        self.assertIn('The sum of 5.0 and 7.0 is: 12.0', captured_output.getvalue())
    
    @patch('builtins.input', side_effect=['abc', '7'])
    def test_main_with_invalid_input(self, mock_input):
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Run the main function
        main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check the output
        self.assertIn('Error: Please enter valid numbers', captured_output.getvalue())

if __name__ == "__main__":
    unittest.main()