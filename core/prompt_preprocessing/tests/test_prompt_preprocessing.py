import unittest
import os
import json
import tempfile
import shutil
from pathlib import Path

from ..prompt_preprocessing import preprocess_prompt

class TestPromptPreprocessing(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test outputs
        self.test_dir = tempfile.mkdtemp()
        self.sample_dir = Path(__file__).parent

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_sample1_processing(self):
        input_file = str(self.sample_dir / 'sample1.txt')
        output_dir = self.test_dir
        
        # Process the file
        preprocess_prompt(input_file, output_dir)
        
        # Check if output file exists
        output_file = os.path.join(output_dir, 'sample1.json')
        self.assertTrue(os.path.exists(output_file))
        
        # Read and verify the JSON content
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Check structure
        self.assertEqual(len(data), 3)  # Should have 3 prompts
        for item in data:
            self.assertEqual(item['type'], 'prompt')
            self.assertIn('contents', item)
            self.assertIsInstance(item['contents'], str)

    def test_sample2_processing(self):
        input_file = str(self.sample_dir / 'sample2.txt')
        output_dir = self.test_dir
        
        # Process the file
        preprocess_prompt(input_file, output_dir)
        
        # Check if output file exists
        output_file = os.path.join(output_dir, 'sample2.json')
        self.assertTrue(os.path.exists(output_file))
        
        # Read and verify the JSON content
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Check structure
        self.assertEqual(len(data), 3)  # Should have 3 prompts
        for item in data:
            self.assertEqual(item['type'], 'prompt')
            self.assertIn('contents', item)
            self.assertIsInstance(item['contents'], str)

if __name__ == '__main__':
    unittest.main() 