"""
A networkX graph that represents the prompt graph. 

Each node has properties:
- opcode - The opcode of the node
- contents - The contents of the node

Opcodes: 
- ro - Read-only files
- prompt - Text prompt to be given to the AI agent
- command - Command to be executed on the code base
- template - A template to seed the epic project. 

Next features to be added:

1. Node classes:
- Unique classes for each opcode node, that hold specific attributes. 
- right now it's just a dictionary. 

"""

import networkx as nx
from typing import Dict, Any, Optional, List
from enum import Enum
from pathlib import Path

class Opcode(Enum):
    READ_ONLY = "ro"
    PROMPT = "prompt"
    COMMAND = "command"
    TEMPLATE = "template"


class Node:
    """
    Base class for all node types.
    When created, it initializes an integer node_id and opcode.
    """
    def __init__(self, node_id: int, opcode: Opcode, contents: Dict[str, Any]):
        """
        Initialize a new Node instance.
        
        Args:
            node_id: Unique identifier for the node
            opcode: The operation code for the node
            contents: Dictionary containing the node's contents
        """
        self.node_id = node_id
        self.opcode = opcode
        self.contents = contents
        self.name = f"{opcode.value}{node_id}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation."""
        return {
            "node_id": self.node_id,
            "opcode": self.opcode.value,
            "contents": self.contents,
            "name": self.name
        }


class EpicIR:
    def __init__(self):
        """Initialize an empty EpicIR graph."""
        self.graph = nx.DiGraph()
        self.next_node_id = 0  # Track the next available node ID

    def add_node(self, opcode: Opcode, contents: Dict[str, Any], operands: Optional[List[str]] = None) -> Node:
        """
        Add a node to the graph with an incremental node ID.
        
        Args:
            opcode: The opcode for the node
            contents: The contents of the node
            operands: Optional list of operand node names to create edges from
            
        Returns:
            The newly created Node instance
        """
        node = Node(self.next_node_id, opcode, contents)
        self.graph.add_node(node.node_id, **node.to_dict())
        
        # Create edges from operands if provided
        if operands:
            for operand_name in operands:
                # Find the node with matching name
                for existing_node_id, node_data in self.graph.nodes(data=True):
                    if node_data.get('name') == operand_name:
                        self.graph.add_edge(existing_node_id, node.node_id)
                        break
        
        self.next_node_id += 1  # Increment the ID counter
        return node

    def add_edge(self, source_id: int, target_id: int) -> None:
        """
        Add an edge between two nodes in the graph.
        
        Args:
            source_id: The ID of the source node
            target_id: The ID of the target node
            
        Raises:
            ValueError: If either source_id or target_id does not exist in the graph
        """
        if not self.graph.has_node(source_id):
            raise ValueError(f"Source node with ID {source_id} does not exist in the graph")
        if not self.graph.has_node(target_id):
            raise ValueError(f"Target node with ID {target_id} does not exist in the graph")
            
        self.graph.add_edge(source_id, target_id)

    def get_edges(self, include_data: bool = False) -> List[tuple]:
        """
        Get all edges in the graph.
        
        Args:
            include_data: If True, includes edge attributes in the result
            
        Returns:
            List of tuples representing edges. Each tuple contains (source_id, target_id)
            and optionally edge attributes if include_data is True.
        """
        return list(self.graph.edges(data=include_data))
    
    def get_nodes(self) -> List[Node]:
        """
        Get all nodes in the graph.
        """
        return list(self.graph.nodes(data=True))
    
    def get_node(self, node_id: int) -> Node:
        """
        Get a node from the graph by its ID.
        """
        return self.graph.nodes[node_id]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the graph to a dictionary representation.
        
        Returns:
            Dictionary representation of the graph
        """
        return nx.node_link_data(self.graph)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EpicIR':
        """
        Create an EpicIR instance from a dictionary representation.
        
        Args:
            data: Dictionary representation of the graph
            
        Returns:
            New EpicIR instance
        """
        instance = cls()
        instance.graph = nx.node_link_graph(data)
        return instance
    
    def print_graph(self, verbose: bool = False) -> None:
        """
        Print the graph in a readable format.
        
        Args:
            verbose: If True, includes the full contents dictionary for each node
            
        Example format: name = opcode operand1 operand2 ...
        Example format for verbose output: name = opcode operand1 operand2 {print full dict of contents}
        """
        
        print("\nEpicIR graph:\n---------------------")
        # Iterate through all nodes in the graph
        for node_id, node_data in self.graph.nodes(data=True):
            # Get the node's name and opcode
            name = node_data['name']
            opcode = node_data['opcode']
            
            # Get all predecessors (operands) of this node
            operands = []
            for pred_id in self.graph.predecessors(node_id):
                pred_name = self.graph.nodes[pred_id]['name']
                operands.append(pred_name)
            
            # Print in the format: name = opcode operand1 operand2 ...
            operands_str = ' '.join(operands)
            if verbose:
                contents_str = str(node_data['contents'])
                print(f"{name} = {opcode} {operands_str} {contents_str}")
            else:
                print(f"{name} = {opcode} {operands_str}")
        
    