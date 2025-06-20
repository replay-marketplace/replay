'''

This is the main test file where all the tests should go. 

The key thing is to check if all the tests passed or failed and then to write the 
work PASSED or FAILED into ../replay/run_pass_fail.txt

'''

import os
import unittest
import io
from logger import Logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        # Create a string IO object to capture logger output
        self.output = io.StringIO()
        self.logger = Logger(level=4, output=self.output)
    
    def test_log_levels(self):
        # Test all log levels
        self.logger.critical("This is a critical message")
        self.logger.error("This is an error message")
        self.logger.warning("This is a warning message")
        self.logger.info("This is an info message")
        self.logger.debug("This is a debug message")
        
        output = self.output.getvalue()
        
        # Check that all messages are in the output
        self.assertIn("[CRITICAL]", output)
        self.assertIn("This is a critical message", output)
        self.assertIn("[ERROR]", output)
        self.assertIn("This is an error message", output)
        self.assertIn("[WARNING]", output)
        self.assertIn("This is a warning message", output)
        self.assertIn("[INFO]", output)
        self.assertIn("This is an info message", output)
        self.assertIn("[DEBUG]", output)
        self.assertIn("This is a debug message", output)
    
    def test_log_level_filtering(self):
        # Test that setting the level filters messages correctly
        self.logger.set_level(2)  # Only show messages with level <= 2
        
        self.logger.critical("Critical message")
        self.logger.error("Error message")
        self.logger.warning("Warning message")
        self.logger.info("Info message - should not appear")
        self.logger.debug("Debug message - should not appear")
        
        output = self.output.getvalue()
        
        self.assertIn("Critical message", output)
        self.assertIn("Error message", output)
        self.assertIn("Warning message", output)
        self.assertNotIn("Info message", output)
        self.assertNotIn("Debug message", output)
    
    def test_indentation(self):
        # Test that messages are properly indented
        self.logger.log("No indent", 0)
        self.logger.log("One space", 1)
        self.logger.log("Two spaces", 2)
        
        output = self.output.getvalue()
        lines = output.strip().split('\n')
        
        # Extract just the message part after the level indicator
        messages = [line.split(']', 1)[1].strip() for line in lines]
        
        self.assertEqual(messages[0], "No indent")
        self.assertEqual(messages[1], " One space")
        self.assertEqual(messages[2], "  Two spaces")

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestLogger)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    passed = run_tests()

    if passed:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("True")
    else:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("False")
