import shutil
import json
import networkx as nx
import logging
from typing import List

from .ir.ir import Opcode, FE_MARKERS, INTRA_NODE_MARKERS
from .ir.ir import nx_draw_graph, Opcode, print_graph, print_graph_to_file, EpicIR
from .parse_prompt import text_to_list2,parse_ir_markers

def bfs_nodes(epic: EpicIR) -> List[str]:
    """
    Get nodes in breadth-first search order using NetworkX's built-in BFS.
    
    Args:
        epic: The EpicIR graph to traverse
        
    Returns:
        List of node names in BFS order
    """
    if not epic.graph.nodes():
        return []
        
    # Get the first node (assuming it's the root)
    start_node = next(iter(epic.graph.nodes()))
    
    # Use NetworkX's built-in BFS to get nodes in order
    return list(nx.bfs_tree(epic.graph, start_node).nodes())

def pass_insert_exit_node(epic: EpicIR) -> EpicIR:
    """Add EXIT node at the end if not already present."""
    print("\n\nPASS: Insert Exit Node")
    
    # Make a node list based on Breadth First Search
    node_list = bfs_nodes(epic)
    print("\n\nNode list:")
    print(node_list)

    # Check all the nodes in the node_list to see if Opcode.EXIT already exists
    for node in node_list:
        if epic.graph.nodes[node]['opcode'] == Opcode.EXIT:
            print(f"Exit node {node} already exists")
            return epic
    
    # If Opcode.EXIT does not exist, add it to the graph
    previous_node = node_list[-1]
    node_name = "exit_node_" + epic.get_next_node_counter()
    epic.graph.add_node(node_name, 
                        opcode=Opcode.EXIT, 
                        contents={})
    epic.graph.add_edge(previous_node, node_name)
    epic.node_counter += 1
    return epic

