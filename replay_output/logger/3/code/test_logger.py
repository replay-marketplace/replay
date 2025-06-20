import unittest
from io import StringIO
import sys
from logger import Logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        # Redirect stdout to capture print output
        self.held_output = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.held_output
        
    def tearDown(self):
        # Reset stdout
        sys.stdout = self.old_stdout
    
    def test_log_levels(self):
        logger = Logger(level=4)  # Set to debug level to show all messages
        logger.critical("This is a critical message")
        logger.error("This is an error message")
        logger.warning("This is a warning message")
        logger.info("This is an info message")
        logger.debug("This is a debug message")
        
        output = self.held_output.getvalue()
        self.assertIn("[CRITICAL]", output)
        self.assertIn("[ERROR]", output)
        self.assertIn("[WARNING]", output)
        self.assertIn("[INFO]", output)
        self.assertIn("[DEBUG]", output)
    
    def test_level_filtering(self):
        logger = Logger(level=2)  # Only show warning and above
        logger.critical("This is a critical message")
        logger.error("This is an error message")
        logger.warning("This is a warning message")
        logger.info("This is an info message")
        logger.debug("This is a debug message")
        
        output = self.held_output.getvalue()
        self.assertIn("[CRITICAL]", output)
        self.assertIn("[ERROR]", output)
        self.assertIn("[WARNING]", output)
        self.assertNotIn("[INFO]", output)
        self.assertNotIn("[DEBUG]", output)
    
    def test_indentation(self):
        logger = Logger(level=4)
        logger.critical("Critical")
        logger.debug("Debug")
        
        output = self.held_output.getvalue().split('\n')
        self.assertTrue(any("[CRITICAL] Critical" in line for line in output))
        self.assertTrue(any("[DEBUG]     Debug" in line for line in output))

if __name__ == "__main__":
    unittest.main()