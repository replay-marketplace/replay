import networkx as nx
from typing import List
from ..ir.ir import Opcode, EpicIR

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

def pass_process_ro_markers(epic: EpicIR) -> EpicIR:
    """Create READ_ONLY nodes from /RO markers in prompt text."""
    
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