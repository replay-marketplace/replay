import shutil
import json
import networkx as nx
import logging
from typing import List

from .ir.ir import Opcode, FE_MARKERS, INTRA_NODE_MARKERS
from .ir.ir import nx_draw_graph, Opcode, print_graph, print_graph_to_file, EpicIR
from .parse_prompt import parse_ir_markers


# parse @command:"cli command with args to be run"
def parse_command(extracted_config: str) -> str:    
    # find @command:
    command_to_run = extracted_config.split("@command:")[1]
    # remove quotes in the start and end if present
    command_to_run = command_to_run.strip('"')
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
    
    print("\n\nPASS: Build Epic Graph:")
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

# Legacy function for backward compatibility
def pass_build_epic_graph_legacy(input_file: str) -> EpicIR:
    """Legacy function that creates a new EpicIR and calls the pass."""
    epic = EpicIR()
    return pass_build_epic_graph(epic, input_file)
