import pytest
import os
import argparse
from prompt_preprocess2.processor3 import prompt_preprocess3

def test_prompt_preprocess2_with_file(input_file, output_dir):
    """Test prompt preprocessing using the provided file path."""
    
    result = prompt_preprocess3(input_file, output_dir)
    return result

def test_prompt_file_refs(tmp_path):
    from prompt_preprocess2.ir.ir import Opcode
    import networkx as nx
    import shutil
    test_file = os.path.join(os.path.dirname(__file__), 'prompt_file_refs.txt')
    output_dir = tmp_path
    shutil.copy(test_file, output_dir)
    epic = prompt_preprocess3(os.path.join(output_dir, 'prompt_file_refs.txt'), str(output_dir))

    # Find all PROMPT nodes
    prompt_nodes = [n for n in epic.graph.nodes() if epic.graph.nodes[n]['opcode'] == Opcode.PROMPT]
    # For each prompt node, check for incoming READ_ONLY nodes with correct contents
    found_refs = []
    for prompt_node in prompt_nodes:
        preds = list(epic.graph.predecessors(prompt_node))
        for pred in preds:
            if epic.graph.nodes[pred]['opcode'] == Opcode.READ_ONLY:
                found_refs.append(epic.graph.nodes[pred]['contents'])
    # Should find all three types and correct file paths
    expected = [
        {'file_path': 'docs1.txt', 'marker': 'docs'},
        {'file_path': 'template1.txt', 'marker': 'template'},
        {'file_path': 'code1.py', 'marker': 'code'},
        {'file_path': 'docs2.txt', 'marker': 'docs'}
    ]
    for e in expected:
        assert e in found_refs, f"Expected ref {e} not found in graph"

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    parser = argparse.ArgumentParser(description='Test prompt preprocessing with a file')
    parser.add_argument('file_path', help='Path to the input file for testing')
    parser.add_argument('output_dir', help='Path to the output directory for testing')
    args = parser.parse_args()
    
    result = test_prompt_preprocess2_with_file(args.file_path, args.output_dir)

if __name__ == "__main__":
    main()
