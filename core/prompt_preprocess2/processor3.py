import shutil
import networkx as nx
import json
import os
from typing import List

from .parse_prompt import extract_template
from .parse_prompt import extract_next_word_after_marker
from .parse_prompt import get_string_from_file

from .ir.ir import Opcode, FE_MARKERS, INTRA_NODE_MARKERS
from .ir.ir import nx_draw_graph, Opcode, print_graph, print_graph_to_file, EpicIR

# Import passes
from .pass_build_graph import pass_build_epic_graph
from .passes import pass_insert_exit_node
from .pass_lower_debug_loop import pass_lower_debug_loop
from .pass_lower_prompt_file_refs import pass_lower_prompt_file_refs
from .pass_process_ro_markers import pass_process_ro_markers

from .pass_registry import PassRegistry

def _save_graph_pass(epic: EpicIR, replay_dir: str, filename: str):
    """
    Save graph after each pass for debugging and analysis.
    
    Args:
        epic: The EpicIR graph to save
        replay_dir: Directory to save the graph file
        filename: Name of the file to save the graph as
    """
    print_graph(epic.graph, True)
    graph_file = os.path.join(replay_dir, filename)
    with open(graph_file, 'w') as f:
        json.dump(epic.to_dict(), f, indent=2)
    print(f"Saved graph after pass: {filename}")

def build_initial_graph(input_file: str) -> EpicIR:
    """
    Build the initial EpicIR graph from the input file.
    This is not a pass - it's the initial graph creation.
    
    Args:
        input_file: Path to the input prompt file
        
    Returns:
        EpicIR: The initial graph
    """
    print("\n\nBUILDING INITIAL GRAPH FROM INPUT FILE")
    epic = EpicIR()
    return pass_build_epic_graph(epic, input_file)

def prompt_preprocess3(input_file: str, replay_dir: str) -> EpicIR:
    """
    Preprocess prompt file using registered passes.
    
    Args:
        input_file: Path to the input prompt file
        replay_dir: Directory to save intermediate graphs and output
        
    Returns:
        EpicIR: The final processed graph
    """
    # Initialize pass registry locally
    pass_registry = PassRegistry()
    
    # Register all passes in desired order
    pass_registry.register(pass_insert_exit_node)
    pass_registry.register(pass_lower_debug_loop)
    pass_registry.register(pass_lower_prompt_file_refs)
    pass_registry.register(pass_process_ro_markers)
    
    # Copy input file to replay directory
    shutil.copy(input_file, replay_dir)
    
    # Step 1: Build initial graph (not a pass)
    epic = build_initial_graph(input_file)
    _save_graph_pass(epic, replay_dir, "initial_graph.json")    
    
    # Step 2: Execute all registered transformation passes
    for i, pass_info in enumerate(pass_registry.get_all_passes(), 1):
        print(f"\n\nPASS: {pass_info.name}")
        if pass_info.description:
            print(f"Description: {pass_info.description}")
        
        # Execute the pass
        epic = pass_info.func(epic)
        
        # Save graph after each pass
        _save_graph_pass(epic, replay_dir, f"pass{i}_{pass_info.name}.json")
        nx_draw_graph(epic.graph, replay_dir, f"pass{i}_{pass_info.name}.png")
        print_graph_to_file(epic.graph, replay_dir, f"pass{i}_{pass_info.name}.txt", True)
    
    return epic