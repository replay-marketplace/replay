'''
This is the main test runner that executes all tests in the tests directory
and writes the result to ../replay/run_pass_fail.txt
'''

import unittest
import os
import sys

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_tests():
    # Discover and run all tests in the tests directory
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.dirname(os.path.abspath(__file__)), pattern="test_*.py")
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return test_result.wasSuccessful()

if __name__ == "__main__":
    passed = run_tests()

    # Create the replay directory if it doesn't exist
    replay_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "replay")
    os.makedirs(replay_dir, exist_ok=True)
    
    # Write the result to run_pass_fail.txt
    result_file = os.path.join(replay_dir, "run_pass_fail.txt")
    with open(result_file, "w") as f:
        if passed:
            f.write("PASSED")
        else:
            f.write("FAILED")