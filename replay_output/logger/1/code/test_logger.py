import io
import unittest
from simple_logger import Logger

class TestLogger(unittest.TestCase):
    def test_log_levels(self):
        # Capture output
        output = io.StringIO()
        
        # Create logger with all levels enabled, no colors for testing
        logger = Logger(min_level=4, use_colors=False, output=output)
        
        # Log messages at different levels
        logger.critical("This is a critical message")
        logger.error("This is an error message")
        logger.warning("This is a warning message")
        logger.info("This is an info message")
        logger.debug("This is a debug message")
        
        # Get the output
        result = output.getvalue()
        
        # Check that all messages were logged
        self.assertIn("[CRITICAL] This is a critical message", result)
        self.assertIn("[ERROR] This is an error message", result)
        self.assertIn("[WARNING]  This is a warning message", result)
        self.assertIn("[INFO]   This is an info message", result)
        self.assertIn("[DEBUG]    This is a debug message", result)
    
    def test_min_level_filtering(self):
        # Test filtering based on min_level
        output = io.StringIO()
        logger = Logger(min_level=2, use_colors=False, output=output)
        
        logger.critical("Critical")
        logger.error("Error")
        logger.warning("Warning")
        logger.info("Info")  # Should not be logged
        logger.debug("Debug")  # Should not be logged
        
        result = output.getvalue()
        
        # These should be logged
        self.assertIn("[CRITICAL] Critical", result)
        self.assertIn("[ERROR] Error", result)
        self.assertIn("[WARNING]  Warning", result)
        
        # These should not be logged
        self.assertNotIn("[INFO]", result)
        self.assertNotIn("[DEBUG]", result)
    
    def test_indentation(self):
        # Test that indentation works correctly
        output = io.StringIO()
        logger = Logger(min_level=4, use_colors=False, output=output)
        
        logger.critical("Critical message")
        logger.debug("Debug message")
        
        result = output.getvalue()
        
        # Critical should have no indentation
        self.assertIn("[CRITICAL] Critical message", result)
        
        # Debug should have 4 spaces indentation
        self.assertIn("[DEBUG]    Debug message", result)

if __name__ == '__main__':
    unittest.main()
