import json
import argparse
from pathlib import Path
from typing import List, Tuple
from .ir.ir import FE_MARKERS, INTRA_NODE_MARKERS

def extract_template(input_file: str) -> str:
    """
    Extract the template from the input file. 
    Look for '/TEMPLATE' and return a single word that comes right after it.   
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    template_index = content.find('/TEMPLATE')
    return content[template_index + len('/TEMPLATE'):].strip().split()[0]
    
def parse_ir_markers(input_file: str) -> List[str]:
    """
    Parse a text file containing markers (/TEMPLATE, /PROMPT, /TEST_LOOP) and create a List of strings with the parsed sections.
    Each section should be the text that comes after any of the markers, and until the next marker is found.
    If there are no markers, return an empty list.
    Don't include the text before the first marker.
    Marker should be included in the list. 
    
    Args:
        input_file (str): Path to the input text file
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if there are any markers
    if not any(marker in content for marker in FE_MARKERS):
        return []
    
    # Find all positions of markers in the content
    marker_positions = []
    for marker in FE_MARKERS:
        pos = 0
        while True:
            pos = content.find(marker, pos)
            if pos == -1:
                break
            marker_positions.append((pos, marker))
            pos += len(marker)
    
    # Sort positions to maintain order
    marker_positions.sort()
    
    # Extract sections between markers
    sections = []
    for i in range(len(marker_positions)):
        start_pos = marker_positions[i][0]  # Changed to include marker
        end_pos = marker_positions[i + 1][0] if i + 1 < len(marker_positions) else len(content)
        section = content[start_pos:end_pos].strip()
        if section:
            sections.append(section)
    
    return sections

def text_to_list2(input_file: str) -> List[str]:
    """
    Parse a text file containing /PROMPT and create a List of strings with the parsed prompts.
    Each prompt should be the text that comes after the word /PROMPT, and until the next /PROMPT is found. 
    If there is no /PROMPT, return an empty list.
    Don't include the text before the first /PROMPT.
    
    Args:
        input_file (str): Path to the input text file
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if there are any /PROMPT markers
    if '/PROMPT' not in content:
        return []
    
    # Split the content by /PROMPT and remove the first element (text before first /PROMPT)
    prompts = content.split('/PROMPT')[1:]
    
    # Remove empty strings and strip whitespace
    prompts = [p.strip() for p in prompts if p.strip()]

    return prompts

def extract_next_word_after_marker(input: str, marker: str) -> List[str]:
    """
    Extract all words that come after each instance of the marker in the input string.
    Returns a list of words found after each marker, or an empty list if the marker is not found
    or if there are no words after any instance.
    """
    if not input or marker not in input:
        return []
    
    found_words = []
    start_index = 0
    
    while True:
        marker_index = input.find(marker, start_index)
        if marker_index == -1:
            break
            
        remaining_text = input[marker_index + len(marker):].strip()
        if remaining_text:
            words = remaining_text.split()
            if words:
                found_words.append(words[0])
        
        start_index = marker_index + len(marker)
    
    return found_words

def get_string_from_file(file_path: str) -> str:
    """
    Read the content of a file and return it as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
