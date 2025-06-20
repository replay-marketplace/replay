import unittest
import sys
import os
import io
from contextlib import redirect_stdout

# Add the parent directory to the path so we can import the main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import python_single_file

class TestHelloWorld(unittest.TestCase):
    def test_main_output(self):
        # Capture stdout
        f = io.StringIO()
        with redirect_stdout(f):
            python_single_file.main()
        
        # Get the output
        output = f.getvalue().strip()
        
        # Check if the output is as expected
        self.assertEqual(output, "Hello, World!")
    
    def test_main_function_exists(self):
        # Check if the main function exists
        self.assertTrue(hasattr(python_single_file, 'main'))
        self.assertTrue(callable(getattr(python_single_file, 'main')))

if __name__ == '__main__':
    unittest.main()