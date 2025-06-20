import unittest
import sys
import os


def run_all_tests():
    """
    Run all tests and return True if all tests pass, False otherwise.
    """
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    passed = run_all_tests()
    
    # Create directory if it doesn't exist
    os.makedirs("../replay", exist_ok=True)
    
    if passed:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("True")
    else:
        with open("../replay/run_tests_pass_fail.txt", "w") as f:
            f.write("False")
    
    # Exit with appropriate code
    sys.exit(0 if passed else 1)
