import os
import json
import argparse
from typing import List, Dict

from core.helpers.utils import debug_print

def code_to_json(input_dir: str) -> List[Dict[str, str]]:
    """
    Convert all files in a directory to a JSON structure.
    
    Args:
        input_dir (str): Path to the input directory
        
    Returns:
        List[Dict[str, str]]: List of dictionaries containing file paths and contents
    """
    
    result = []
    DEBUG = False
    INDENT = 4

    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            debug_print(f"SUS -->>root, file: {root}   {file}", INDENT, DEBUG)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.read()
                    
                result.append({
                    "path_and_filename": file,
                    "contents": contents
                })
            except Exception as e:
                debug_print(f"Error reading file {file_path}: {str(e)}", INDENT, DEBUG)
                
    return result

def main():
    parser = argparse.ArgumentParser(description='Convert directory contents to JSON')
    parser.add_argument('input_dir', help='Input directory to convert')
    parser.add_argument('output_dir', help='Output directory for JSON file')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Convert directory to JSON
    result = code_to_json(args.input_dir)
    
    # Save to file
    output_file = os.path.join(args.output_dir, 'output.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    print(f"JSON file created at: {output_file}")

if __name__ == "__main__":
    main() 