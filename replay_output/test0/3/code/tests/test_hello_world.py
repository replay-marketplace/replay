import unittest
import io
import sys
from unittest.mock import patch
import hello_world

class TestHelloWorld(unittest.TestCase):
    def test_main_output(self):
        # Redirect stdout to capture the output
        captured_output = io.StringIO()
        with patch('sys.stdout', new=captured_output):
            hello_world.main()
        
        # Get the printed output
        output = captured_output.getvalue().strip()
        
        # Assert the output is as expected
        self.assertEqual(output, "Hello, World!")

if __name__ == "__main__":
    unittest.main()