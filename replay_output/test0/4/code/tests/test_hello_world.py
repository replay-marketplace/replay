import unittest
import sys
import io
from contextlib import redirect_stdout
import hello_world

class TestHelloWorld(unittest.TestCase):
    def test_main_output(self):
        # Redirect stdout to capture print output
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            hello_world.main()
        
        # Check if the output matches expected
        self.assertEqual(captured_output.getvalue().strip(), "Hello, World!")

if __name__ == "__main__":
    unittest.main()