import shutil
import json
import networkx as nx
import logging
from typing import List

from .ir.markers import FE_MARKERS
from .ir.ir import Opcode, EpicIR

# parse @command:"cli command with args to be run"
def parse_command(extracted_config: str) -> str:    
    # find @command:
    command_to_run = extracted_config.split("@command:")[1]
    # remove quotes in the start and end if present
    command_to_run = command_to_run.strip('"').strip(" ")
    return command_to_run

def add_simple_edge(epic: EpicIR, previous_node: str, new_node: str):
    if previous_node is not None:
        epic.graph.add_edge(previous_node, new_node)
    previous_node = new_node
    return previous_node

def pass_build_epic_graph(epic: EpicIR, input_file: str = None) -> EpicIR:
    """Build initial EpicIR graph from input file markers."""
    if input_file is None:
        raise ValueError("input_file is required for build_graph pass")
    
    ir_marker_list = parse_ir_markers(input_file)
    #print("\n\nir_marker_list:")
    #print(ir_marker_list)

    previous_node = None
    for ir_marker in ir_marker_list:
        
        # Parsing the text         
        ir_marker_first_word = ir_marker.split()[0]
        ir_marker_without_first_word = " ".join(ir_marker.split()[1:])  # Join remaining words into a string

        if ir_marker_first_word == "/TEMPLATE":
            new_node = epic.add_node(opcode=Opcode.TEMPLATE, contents={"path": ir_marker_without_first_word})
            previous_node = add_simple_edge(epic, previous_node, new_node)
        
        elif ir_marker_first_word == "/DOCS":
            new_node = epic.add_node(opcode=Opcode.DOCS, contents={"path": ir_marker_without_first_word})
            previous_node = add_simple_edge(epic, previous_node, new_node)
        
        elif ir_marker_first_word == "/PROMPT":
            new_node = epic.add_node(opcode=Opcode.PROMPT, contents={"prompt": ir_marker_without_first_word})
            previous_node = add_simple_edge(epic, previous_node, new_node) 
       
        elif ir_marker_first_word == "/RUN":
            new_node = epic.add_node(opcode=Opcode.RUN, contents={"command": parse_command(ir_marker_without_first_word)})
            previous_node = add_simple_edge(epic, previous_node, new_node)

        elif ir_marker_first_word == "/DEBUG_LOOP":
            new_node = epic.add_node(opcode=Opcode.DEBUG_LOOP, contents={"command": parse_command(ir_marker_without_first_word)})
            previous_node = add_simple_edge(epic, previous_node, new_node)

        elif ir_marker_first_word == "/EXIT":
            new_node = epic.add_node(opcode=Opcode.EXIT, contents={})
            previous_node = add_simple_edge(epic, previous_node, new_node)    

    return epic

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