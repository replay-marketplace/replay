import json
import os
from typing import Dict, List, Union

from helpers.utils import debug_print

def json_to_code(output_dir: str, json_data: Union[Dict, List]) -> None:
    """
    Process JSON data and generate files in the specified output directory.
    
    Args:
        output_dir (str): Directory where files will be generated
        json_data (Union[Dict, List]): JSON data containing file information
    """
    
    DEBUG = False
    INDENT = 4
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Handle both single file and array of files
    files_data = json_data if isinstance(json_data, list) else [json_data]
    debug_print(f"\n\nfiles_data: {files_data}", INDENT, DEBUG)
    for file_info in files_data:
        if not isinstance(file_info, dict):
            continue
            
        path_and_filename = file_info.get('path_and_filename')
        contents = file_info.get('contents')
        
        if not path_and_filename or not contents:
            continue
            
        # Create full path
        full_path = os.path.join(output_dir, path_and_filename)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(contents)

if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate files from JSON input')
    parser.add_argument('output_dir', help='Output directory for generated files')
    parser.add_argument('input_file', help='Input JSON file')
    
    args = parser.parse_args()
    
    with open(args.input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    json_to_code(args.output_dir, json_data) 