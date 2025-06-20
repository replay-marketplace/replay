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