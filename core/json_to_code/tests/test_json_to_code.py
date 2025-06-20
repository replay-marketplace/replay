import unittest
import os
import json
import shutil
from ..json_to_code import json_to_code

class TestJsonToCode(unittest.TestCase):
    def setUp(self):
        self.test_output_dir = "test_output"
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        os.makedirs(self.test_output_dir)

    def tearDown(self):
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)

    def test_single_file(self):
        with open("test1.json", "r") as f:
            json_data = json.load(f)
        
        json_to_code(self.test_output_dir, json_data)
        
        # Check if file was created
        self.assertTrue(os.path.exists(os.path.join(self.test_output_dir, "hello.txt")))
        
        # Check contents
        with open(os.path.join(self.test_output_dir, "hello.txt"), "r") as f:
            contents = f.read()
        self.assertEqual(contents, "Hello, World!")

    def test_nested_structure(self):
        with open("test2.json", "r") as f:
            json_data = json.load(f)
        
        json_to_code(self.test_output_dir, json_data)
        
        # Check if files were created
        self.assertTrue(os.path.exists(os.path.join(self.test_output_dir, "src/main.py")))
        self.assertTrue(os.path.exists(os.path.join(self.test_output_dir, "src/utils/helper.py")))
        
        # Check contents
        with open(os.path.join(self.test_output_dir, "src/main.py"), "r") as f:
            contents = f.read()
        self.assertIn("def main()", contents)
        
        with open(os.path.join(self.test_output_dir, "src/utils/helper.py"), "r") as f:
            contents = f.read()
        self.assertIn("def helper()", contents)

    def test_single_object(self):
        with open("test3.json", "r") as f:
            json_data = json.load(f)
        
        json_to_code(self.test_output_dir, json_data)
        
        # Check if file was created
        self.assertTrue(os.path.exists(os.path.join(self.test_output_dir, "config.json")))
        
        # Check contents
        with open(os.path.join(self.test_output_dir, "config.json"), "r") as f:
            contents = f.read()
        self.assertIn("setting1", contents)
        self.assertIn("value1", contents)

if __name__ == '__main__':
    unittest.main() 