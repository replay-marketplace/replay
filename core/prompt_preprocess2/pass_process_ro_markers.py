import networkx as nx
from typing import List
from .ir.ir import Opcode, EpicIR
from .parse_prompt import extract_next_word_after_marker

def pass_process_ro_markers(epic: EpicIR) -> EpicIR:
    """Create READ_ONLY nodes from /RO markers in prompt text."""
    print("\n\nPASS: Process RO Markers")
    
    # Loop over nodes in NetworkX graph
    offline_node_list = list(epic.graph.nodes())
    ro_count = 0

    for node in offline_node_list:
        # If node opcode is Opcode.PROMPT, process RO markers
        if epic.graph.nodes[node]['opcode'] == Opcode.PROMPT:
            prompt = epic.graph.nodes[node]['contents']['prompt']

            # Extract all RO words from the prompt
            ro_list = extract_next_word_after_marker(prompt, "/RO")

            for ro in ro_list:
                if ro != "":
                    node_ro = f"ro_{ro_count}"
                    ro_count += 1
                    epic.graph.add_node(node_ro, opcode=Opcode.READ_ONLY, contents={"path": ro})

                    # Add an edge from the node_ro to the node_prompt
                    epic.graph.add_edge(node_ro, node)

                    # Store the RO folder path in the prompt node's contents
                    epic.graph.nodes[node]['contents']['ro_folder'] = ro
    
    return epic 