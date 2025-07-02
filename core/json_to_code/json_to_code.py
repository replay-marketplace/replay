import json
import os
import logging
from typing import Dict, List, Union
from pathlib import Path

from core.helpers.utils import debug_print

logger = logging.getLogger(__name__)

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
    logger.debug(f"Writing files to output directory: {output_dir}")
    
    # Handle both single file and array of files
    files_data = json_data if isinstance(json_data, list) else [json_data]
    debug_print(f"\n\nfiles_data: {files_data}", INDENT, DEBUG)
    
    processed_files = []
    for file_info in files_data:
        if not isinstance(file_info, dict):
            logger.warning(f"Skipping non-dict file_info: {file_info}")
            continue
            
        path_and_filename = file_info.get('path_and_filename')
        contents = file_info.get('contents')
        
        if not path_and_filename:
            logger.warning(f"Skipping file_info without path_and_filename: {file_info}")
            continue
            
        if contents is None:
            logger.warning(f"Skipping file_info without contents: {file_info}")
            continue
            
        # Create full path using Path for better cross-platform compatibility
        full_path = Path(output_dir) / path_and_filename
        
        # Create directory if it doesn't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Write file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(contents)
            
            processed_files.append(str(full_path))
            logger.debug(f"Successfully wrote file: {full_path}")
            
        except Exception as e:
            logger.error(f"Error writing file {full_path}: {str(e)}")
            raise
    
    logger.info(f"Processed {len(processed_files)} files: {processed_files}")

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