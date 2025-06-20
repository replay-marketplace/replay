import unittest
import os
import sys

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_adder import TestAdder

def run_all_tests():
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add all tests from TestAdder
    test_suite.addTest(unittest.makeSuite(TestAdder))
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return True if all tests passed, False otherwise
    return result.wasSuccessful()

if __name__ == "__main__":
    passed = run_all_tests()
    
    # Create the replay directory if it doesn't exist
    replay_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "replay")
    os.makedirs(replay_dir, exist_ok=True)
    
    # Write the result to file
    result_file = os.path.join(replay_dir, "run_tests_pass_fail.txt")
    with open(result_file, "w") as f:
        f.write(str(passed))
    
    print(f"Tests {'passed' if passed else 'failed'}")
    sys.exit(0 if passed else 1)
