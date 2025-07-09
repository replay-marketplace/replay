import networkx as nx
from ..ir.ir import Opcode, EpicIR

import re

def pass_lower_prompt_file_refs(epic: EpicIR) -> EpicIR:
    """Extract @docs:, @template:, and @code: references from prompt text."""

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
            # Deduplicate references
            refs = list(dict.fromkeys(refs))  # Preserves order while deduplicating
            
            # Append to existing refs if they exist, otherwise create new list
            existing_refs = prompt_contents.get(f'{marker}_refs', [])
            if existing_refs:
                # Combine and deduplicate
                combined_refs = existing_refs + refs
                prompt_contents[f'{marker}_refs'] = list(dict.fromkeys(combined_refs))
            else:
                prompt_contents[f'{marker}_refs'] = refs
                
            if refs:
                print(f"Added {marker}_refs to {prompt_node}: {refs}")
        # Optionally, you could remove the marker from the prompt text here if desired
        # (not implemented)

    # Parsing runs referenced into this prompt
    # This allows to later load the run logs files into the prompt node
    # We can't link the run logs files to the prompt node in the graph because
    # those are dynamically created during execution and can have files from multiple runs 
    run_ref_pattern = re.compile(r'@run_ref:([^\s]+)')
    for prompt_node in prompt_nodes:
        prompt_contents = epic.graph.nodes[prompt_node]['contents']
        prompt_text = prompt_contents.get('prompt', '')
        refs = [match.strip() for match in run_ref_pattern.findall(prompt_text)]
        # Deduplicate references
        refs = list(dict.fromkeys(refs))  # Preserves order while deduplicating
        
        # Append to existing refs if they exist, otherwise create new list
        existing_refs = prompt_contents.get('run_refs', [])
        if existing_refs:
            # Combine and deduplicate
            combined_refs = existing_refs + refs
            prompt_contents['run_refs'] = list(dict.fromkeys(combined_refs))
        else:
            prompt_contents['run_refs'] = refs
            
        if refs:
            print(f"Added run_refs to {prompt_node}: {refs}")

    return epic 