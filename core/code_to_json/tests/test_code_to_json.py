import unittest
import os
import json
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))
from code_to_json import code_to_json

class TestCodeToJson(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(__file__).parent
        self.test1_dir = self.test_dir / "test1"
        self.test2_dir = self.test_dir / "test2"
        self.test3_dir = self.test_dir / "test3"
        
    def test_test1_directory(self):
        """Test conversion of test1 directory"""
        result = code_to_json(str(self.test1_dir))
        print("\nTest1 JSON output:")
        print(json.dumps(result, indent=2))
        self.assertEqual(len(result), 1)
        self.assertTrue(any("file1.py" in item["path_and_filename"] for item in result))
        
    def test_test2_directory(self):
        """Test conversion of test2 directory with nested structure"""
        result = code_to_json(str(self.test2_dir))
        print("\nTest2 JSON output:")
        print(json.dumps(result, indent=2))
        self.assertEqual(len(result), 2)
        self.assertTrue(any("nested/file2.py" in item["path_and_filename"] for item in result))
        
    def test_test3_directory(self):
        """Test conversion of test3 directory with text file"""
        result = code_to_json(str(self.test3_dir))
        print("\nTest3 JSON output:")
        print(json.dumps(result, indent=2))
        self.assertEqual(len(result), 1)
        self.assertTrue(any("file1.txt" in item["path_and_filename"] for item in result))

if __name__ == '__main__':
    unittest.main() 