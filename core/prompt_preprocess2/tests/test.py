import pytest
import os
import argparse
from prompt_preprocess2.processor3 import prompt_preprocess3

def test_prompt_preprocess2_with_file(input_file, output_dir):
    """Test prompt preprocessing using the provided file path."""
    
    result = prompt_preprocess3(input_file, output_dir)
    return result

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    parser = argparse.ArgumentParser(description='Test prompt preprocessing with a file')
    parser.add_argument('file_path', help='Path to the input file for testing')
    parser.add_argument('output_dir', help='Path to the output directory for testing')
    args = parser.parse_args()
    
    result = test_prompt_preprocess2_with_file(args.file_path, args.output_dir)

if __name__ == "__main__":
    main()
