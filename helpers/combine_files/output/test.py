# Combine Files

A simple Python utility that combines multiple files into a single output file while preserving their order.

## Usage

```bash
python combine_files.py [input_files...] --output-dir OUTPUT_DIR --output-filename OUTPUT_FILENAME
```

### Arguments

- `input_files`: One or more input files to combine (required)
- `--output-dir` or `-o`: Directory where the output file will be created (required)
- `--output-filename` or `-f`: Name of the output file (required)

### Example

```bash
# Combine three text files into a single output file
python combine_files.py file1.txt file2.txt file3.txt --output-dir output --output-filename combined.txt

# Using short options
python combine_files.py file1.txt file2.txt file3.txt -o output -f combined.txt
```

## Features

- Combines multiple files in the specified order
- Creates output directory if it doesn't exist
- Handles UTF-8 encoding
- Adds newlines between files if needed
- Provides error handling for individual files
- Preserves file order as specified in the command line

## Requirements

- Python 3.x
- No external dependencies required 
#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

def combine_files(input_files, output_dir, output_filename):
    """
    Combine multiple files into a single output file.
    
    Args:
        input_files (list): List of input file paths
        output_dir (str): Directory where the output file will be created
        output_filename (str): Name of the output file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the full output path
    output_path = os.path.join(output_dir, output_filename)
    
    # Open the output file in write mode
    with open(output_path, 'w', encoding='utf-8') as outfile:
        # Process each input file
        for input_file in input_files:
            try:
                with open(input_file, 'r', encoding='utf-8') as infile:
                    # Read and write the entire content
                    content = infile.read()
                    outfile.write(content)
                    # Add a newline between files if the content doesn't end with one
                    if content and not content.endswith('\n'):
                        outfile.write('\n')
            except Exception as e:
                print(f"Error processing file {input_file}: {str(e)}")
                continue

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Combine multiple files into a single output file')
    parser.add_argument('input_files', nargs='+', help='List of input files to combine')
    parser.add_argument('--output-dir', '-o', required=True, help='Output directory path')
    parser.add_argument('--output-filename', '-f', required=True, help='Output filename')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Combine the files
    combine_files(args.input_files, args.output_dir, args.output_filename)
    print(f"Files combined successfully. Output saved to: {os.path.join(args.output_dir, args.output_filename)}")

if __name__ == '__main__':
    main() 
