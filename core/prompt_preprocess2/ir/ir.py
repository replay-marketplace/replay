import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum
import os
import graphviz

def debug_print(message: str, indent: int = 0, DEBUG: bool = True):
    if DEBUG:
        print(" " * indent + message)


class Opcode(Enum):
    
    # First pass IR markers
    TEMPLATE    = "TEMPLATE"        # 1
    PROMPT      = "PROMPT"          # 2
    READ_ONLY   = "READ_ONLY"       # 3
    DOCS        = "DOCS"            # 4
    RUN         = "RUN"             # 6
    DEBUG_LOOP  = "DEBUG_LOOP"      # 5
    CONDITIONAL = "CONDITIONAL"     # 7
    EXIT        = "EXIT"            # 8

    # Not used yet. 
    COMMAND     = "RUN_COMMAND"     # 4



OPCODE_COLORS = {
    Opcode.TEMPLATE: 'red',
    Opcode.PROMPT: 'blue',
    Opcode.READ_ONLY: 'green',
    Opcode.DOCS: 'cyan',
    Opcode.RUN: 'purple',
    Opcode.DEBUG_LOOP: 'yellow',
    Opcode.COMMAND: 'red',
    Opcode.CONDITIONAL: 'orange',
    Opcode.EXIT: 'brown'
    }


# Front End parser: parse User input prompt.txt file markers
# ToDo: rensme to FE_MARKERS
FE_MARKERS = [    "/TEMPLATE",      # 1
                  "/PROMPT",        # 2
                  "/DOCS",          # 4
                  "/RUN",           # 4
                  "/DEBUG_LOOP", 
                  "/EXIT"]    # 3 Lowered into a conditional loop 

# Markers within a node after the IR_MARKER parsing, that trigger second order effects
INTRA_NODE_MARKERS = ["/RO"]


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
        if name is None:
            node_name = opcode.value.lower() + "_" + self.get_next_node_counter()
        else:
            node_name = name + "_" + self.get_next_node_counter()

        self.graph.add_node(node_name,opcode=opcode, contents=contents)
        if self.first_node is None:
            self.first_node = node_name
        return node_name

    def to_dict(self) -> dict:
        """
        Convert the EpicIR to a dictionary representation for JSON serialization.
        """
        return {
            'first_node': self.first_node,
            'node_counter': self.node_counter,
            'graph': nx.node_link_data(self.graph)
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
            instance.graph = nx.node_link_graph(data['graph'])
        return instance





# ------------------------------------------------------------
#                       Control Flow Traversal
# ------------------------------------------------------------
def cfg_traversal_init_queue(epic: EpicIR) -> list:
    queue = []
    queue.append(epic.first_node)
    return queue


def cfg_traversal_step(epic: EpicIR, queue: list) -> tuple[list, str]:
    DEBUG = False
    INDENT = 2

    current_node = queue.pop()
    debug_print(f"\nCurrent node: {current_node}", INDENT, DEBUG)
    
    # Check if the node is a CONDITIONAL node
    if epic.graph.nodes[current_node]['opcode'] == Opcode.CONDITIONAL:
        debug_print(f"Found CONDITIONAL node: {current_node}", INDENT + 2, DEBUG)
        cond_contents = epic.graph.nodes[current_node]['contents']
        
        # Increment the iteration count
        cond_contents['iteration_count'] += 1
        if cond_contents['iteration_count'] >= cond_contents['iteration_max']:
            queue.append(epic.graph.nodes[current_node]['contents']['true_node_target'])
        else:
            if epic.graph.nodes[current_node]['contents']['condition']:    
                queue.append(epic.graph.nodes[current_node]['contents']['true_node_target'])
            else:
                queue.append(epic.graph.nodes[current_node]['contents']['false_node_target'])
    
    # All other nodes
    else:
        successors = list(epic.graph.successors(current_node))
        debug_print(f"Adding successors to queue: {successors}", INDENT + 2, DEBUG)
        queue.extend(successors)
    
    
    debug_print(f"Current queue: {queue}", INDENT + 2, DEBUG)

    return queue, current_node

# ------------------------------------------------------------
#                 Graph Visualization & Printing
# ------------------------------------------------------------

def nx_draw_graph(graph: nx.DiGraph, file_path: str, file_name: str) -> None:
    """
    Draw a directed graph using networkx and matplotlib and save it to the local folder.
    
    Args:
        graph: The directed graph to visualize
    """
    plt.figure(figsize=(8, 10))

    # Use simple spring layout
    pos = nx.spring_layout(graph)

    # Define color mapping for opcodes
    

    # Create a list of colors for each node based on its opcode
    node_colors = [OPCODE_COLORS[graph.nodes[node]['opcode']] for node in graph.nodes()]

    # Draw the graph
    nx.draw(graph, pos, with_labels=True, node_color=node_colors,
            node_size=2000, arrowsize=20, font_size=10)

    plt.title("Graph Visualization", size=16)
    plt.axis('off')

    plt.savefig(os.path.join(file_path, file_name), dpi=300, bbox_inches='tight')
    plt.close()



def print_graph_to_file(graph: nx.DiGraph, file_path: str, file_name: str, verbose: bool = False) -> None:
    """
    Print the graph to a file.
    """

    graph_string = get_graph_string(graph, verbose)

    with open(os.path.join(file_path, file_name), "w") as f:
        f.write(graph_string)

def print_graph(graph: nx.DiGraph, verbose: bool = False) -> None:
    """
    Print the graph to the terminal.
    """
    graph_string = get_graph_string(graph, verbose)
    
    print(graph_string)


def get_graph_string(graph: nx.DiGraph, verbose: bool = False) -> str:
    """
    Print the graph to the terminal.
    Example otuput format:

    verbose = False
    node_name_0 = opcode(operand1, operand2) ...
    node_name_1 = opcode(operand1, operand2) ...

    verbose = True
    node_name_0 = opcode(operand1, operand2) {contents}
    node_name_1 = opcode(operand1, operand2) {contents}
    
    ... 
    """

    graph_string = "\n"
    for node in graph.nodes():
        # Get node attributes
        node_data = graph.nodes[node]
        opcode = node_data.get('opcode', 'UNKNOWN')
        contents = node_data.get('contents', '')
        
        # Get operands (successors of the node)
        operands = list(graph.predecessors(node))
        
        # Format and print the node information
        operands_str = ', '.join(str(op) for op in operands)
        if verbose:
            graph_string += f"{node} = {opcode}({operands_str}) {{{contents}}}\n"
        else:
            graph_string += f"{node} = {opcode}({operands_str})\n"
    
    return graph_string
    


