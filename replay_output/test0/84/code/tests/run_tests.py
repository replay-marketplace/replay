import unittest
import os
import sys

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_add_numbers import TestAddNumbers

def run_all_tests():
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add the test cases
    test_suite.addTest(unittest.makeSuite(TestAddNumbers))
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return True if all tests passed, False otherwise
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    
    # Create the directory if it doesn't exist
    os.makedirs("../replay", exist_ok=True)
    
    # Write the result to the file
    with open("../replay/run_tests_pass_fail.txt", "w") as f:
        f.write(str(success))
