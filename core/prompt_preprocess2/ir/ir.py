import networkx as nx
from enum import Enum
import os
import graphviz


class Opcode(Enum):
    
    # First pass IR markers
    TEMPLATE    = "TEMPLATE"        # 1
    PROMPT      = "PROMPT"          # 2
    READ_ONLY   = "READ_ONLY"       # 3
    DOCS        = "DOCS"            # 4
    RUN         = "RUN"             # 6
    DEBUG_LOOP  = "DEBUG_LOOP"      # 5
    CONDITIONAL = "CONDITIONAL"     # 7
    FIX         = "FIX"             # 8
    EXIT        = "EXIT"            # 9

def get_node_name(node) -> str:
    return node.get('name', '')

class EpicIR():
    first_node = None
    graph = None
    node_counter = 0

    def __init__(self):
        self.graph = nx.DiGraph()
    
    def set_first_node(self, first_node):
        self.first_node = first_node

    def get_next_node_counter(self) -> str:
        self.node_counter +=1
        return str(self.node_counter)
        
    def add_node(self, opcode: Opcode, contents: dict = {}, name: str = None) -> str:
        id = self.get_next_node_counter()
        if name is None:
            node_name = opcode.value.lower() + "_" + id
        else:
            node_name = name + "_" + id

        self.graph.add_node(node_name, opcode=opcode, contents=contents, id=id)
        if self.first_node is None:
            self.first_node = node_name
        return node_name

    def to_dict(self) -> dict:
        """
        Convert the EpicIR to a dictionary representation for JSON serialization.
        """
        # Make a copy of the graph with opcodes as strings
        graph_copy = self.graph.copy()
        for node in graph_copy.nodes:
            opcode = graph_copy.nodes[node].get('opcode')
            if isinstance(opcode, Opcode):
                graph_copy.nodes[node]['opcode'] = opcode.value
        return {
            'first_node': self.first_node,
            'node_counter': self.node_counter,
            'graph': nx.node_link_data(graph_copy)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'EpicIR':
        """
        Create an EpicIR instance from a dictionary representation.
        """
        instance = cls()
        instance.first_node = data.get('first_node')
        instance.node_counter = data.get('node_counter', 0)
        if 'graph' in data:
            graph = nx.node_link_graph(data['graph'])
            # Restore opcodes as enums
            for node in graph.nodes:
                opcode = graph.nodes[node].get('opcode')
                if isinstance(opcode, str):
                    try:
                        graph.nodes[node]['opcode'] = Opcode(opcode)
                    except ValueError:
                        pass  # Leave as string if not a valid Opcode
            instance.graph = graph
        return instance