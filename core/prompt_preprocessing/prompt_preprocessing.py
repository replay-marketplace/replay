import json
import argparse
import os
from typing import List, Dict

def preprocess_prompt(input_file: str, output_dir: str) -> None:
    """
    Process a text file containing prompts and create a JSON file with the processed prompts.
    
    Args:
        input_file (str): Path to the input text file
        output_dir (str): Directory where the output JSON file will be saved
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the content by \PROMPT
    prompts = content.split('\\PROMPT')
    
    # Remove empty strings and strip whitespace
    prompts = [p.strip() for p in prompts if p.strip()]
    
    # Create JSON structure according to schema
    json_data = []
    for prompt in prompts:
        json_data.append({
            "type": "prompt",
            "contents": prompt
        })
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename based on input filename
    input_filename = os.path.basename(input_file)
    output_filename = os.path.splitext(input_filename)[0] + '.json'
    output_path = os.path.join(output_dir, output_filename)
    
    # Write JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Process a text file containing prompts and create a JSON file.')
    parser.add_argument('input_file', help='Path to the input text file')
    parser.add_argument('output_dir', help='Directory where the output JSON file will be saved')
    
    args = parser.parse_args()
    preprocess_prompt(args.input_file, args.output_dir)

if __name__ == '__main__':
    main() 