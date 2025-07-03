import shutil
import networkx as nx
import json
import os
from typing import List

from .ir.ir import EpicIR
from .ir.graph_visualization import nx_draw_graph, print_graph, print_graph_to_file

# Import passes
from .pass_build_graph import pass_build_epic_graph
from .passes.pass_insert_exit_node import pass_insert_exit_node
from .passes.pass_lower_debug_loop import pass_lower_debug_loop
from .passes.pass_lower_prompt_file_refs import pass_lower_prompt_file_refs
from .passes.pass_process_ro_markers import pass_process_ro_markers

from .passes.pass_registry import PassRegistry

def _save_graph_pass(epic: EpicIR, replay_dir: str, filename_base: str):
    """
    Save graph after each pass for debugging and analysis in all formats.
    
    Args:
        epic: The EpicIR graph to save
        replay_dir: Directory to save the graph files
        filename_base: Base name for the files (without extension)
        save_passes: Whether to actually save the pass files
    """

    print_graph(epic.graph, True)
    
    # Save JSON format
    json_file = os.path.join(replay_dir, f"{filename_base}.json")
    with open(json_file, 'w') as f:
        json.dump(epic.to_dict(), f, indent=2)
    
    nx_draw_graph(epic.graph, replay_dir, f"{filename_base}.png")
    print_graph_to_file(epic.graph, replay_dir, f"{filename_base}.txt", True)


def build_initial_graph(input_file: str) -> EpicIR:
    """
    Build the initial EpicIR graph from the input file.
    This is not a pass - it's the initial graph creation.
    
    Args:
        input_file: Path to the input prompt file
        
    Returns:
        EpicIR: The initial graph
    """
    print("\nBUILDING INITIAL GRAPH FROM INPUT FILE")
    epic = EpicIR()
    return pass_build_epic_graph(epic, input_file)

def prompt_preprocess3(input_file: str, replay_dir: str, save_passes: bool = False) -> EpicIR:
    """
    Process a prompt file through all registered transformation passes.
    
    Args:
        input_file: Path to the input prompt file
        replay_dir: Directory to save intermediate and final files
        save_passes: Whether to save pass files for each transformation
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
    
    # Create passes subdirectory
    passes_dir = os.path.join(replay_dir, "passes")
    os.makedirs(passes_dir, exist_ok=True)
    
    # Copy input file to replay directory
    shutil.copy(input_file, os.path.join(replay_dir, "prompt.txt"))
    
    # Step 1: Parse the prompt file into initial graph
    epic = build_initial_graph(input_file)
    
    # Save initial graph as pass0 in passes/ directory
    if save_passes:
        _save_graph_pass(epic, passes_dir, "pass0_initial_graph")
    
    # Step 2: Execute all registered transformation passes
    for i, pass_info in enumerate(pass_registry.get_all_passes(), 1):
        print(f"\nPASS: {pass_info.name}")
        if pass_info.description: 
            description = pass_info.description.split('\n')[0]
            print(f"Description: {description}")
        
        # Execute the pass
        epic = pass_info.func(epic)
        
        # Save graph after each pass in passes/ subdirectory
        if save_passes:
            _save_graph_pass(epic, passes_dir, f"pass{i}_{pass_info.name}")
    
    # Step 3: Generate final graph visualization files (overwrite initial ones)
    _save_graph_pass(epic, replay_dir, "epic")
    
    return epic