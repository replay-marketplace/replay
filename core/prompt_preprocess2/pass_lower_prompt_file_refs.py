import networkx as nx
from .ir.ir import Opcode, EpicIR

import re

def pass_lower_prompt_file_refs(epic: EpicIR) -> EpicIR:
    print("\n\nPASS: Lower Prompt File References")

    # Regex patterns for the file reference markers
    patterns = {
        'docs': re.compile(r'@docs:([^\s]+)'),
        'template': re.compile(r'@template:([^\s]+)'),
        'code': re.compile(r'@code:([^\s]+)')
    }

    # Find all PROMPT nodes
    prompt_nodes = [node for node in epic.graph.nodes() if epic.graph.nodes[node]['opcode'] == Opcode.PROMPT]

    for prompt_node in prompt_nodes:
        prompt_contents = epic.graph.nodes[prompt_node]['contents']
        prompt_text = prompt_contents.get('prompt', '')
        new_predecessors = []

        # For each marker, find all matches and create new nodes
        for marker, pattern in patterns.items():
            for match in pattern.findall(prompt_text):
                file_path = match.strip()
                # Create a new node for this file reference
                node_contents = {'file_path': file_path, 'marker': marker}
                new_node = epic.add_node(opcode=Opcode.READ_ONLY, contents=node_contents)
                new_predecessors.append(new_node)
                # Connect the new node to the PROMPT node
                epic.graph.add_edge(new_node, prompt_node)
                print(f"Added {marker} node for {file_path} -> {prompt_node}")

        # Optionally, you could remove the marker from the prompt text here if desired
        # (not implemented)

    return epic 