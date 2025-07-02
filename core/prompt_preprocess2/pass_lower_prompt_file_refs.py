import networkx as nx
from .ir.ir import Opcode, EpicIR

import re

def pass_lower_prompt_file_refs(epic: EpicIR) -> EpicIR:
    """Extract @docs:, @template:, and @code: references from prompt text."""
    print("\n\nPASS: Lower Prompt File References")

    # Regex patterns for the file reference markers
    patterns = {
        'docs': re.compile(r'@docs:([^\s]+)'),
        'template': re.compile(r'@template:([^\s]+)'),
        'code': re.compile(r'@code:([^\s]+)'),
        'run_logs': re.compile(r'@run_logs:([^\s]+)')
    }

    # Find all PROMPT nodes
    prompt_nodes = [node for node in epic.graph.nodes() if epic.graph.nodes[node]['opcode'] == Opcode.PROMPT]

    for prompt_node in prompt_nodes:
        prompt_contents = epic.graph.nodes[prompt_node]['contents']
        prompt_text = prompt_contents.get('prompt', '')
        # Store refs in the prompt node's contents
        for marker, pattern in patterns.items():
            refs = [match.strip() for match in pattern.findall(prompt_text)]
            prompt_contents[f'{marker}_refs'] = refs
            if refs:
                print(f"Added {marker}_refs to {prompt_node}: {refs}")
        # Optionally, you could remove the marker from the prompt text here if desired
        # (not implemented)

    return epic 