import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum
import os
import graphviz
from loguru import logger
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrowPatch
import numpy as np

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
<<<<<<< Updated upstream
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
=======
    Opcode.TEMPLATE:   '#FFB3BA',  # soft pink
    Opcode.PROMPT:     '#BAE1FF',  # soft blue
    Opcode.READ_ONLY:  '#BFFCC6',  # soft green
    Opcode.DOCS:       '#FFFFBA',  # soft yellow
    Opcode.RUN:        '#D5BAFF',  # soft lavender
    Opcode.DEBUG_LOOP: '#FFDFBA',  # soft orange
    Opcode.COMMAND:    '#B2F0E6',  # soft teal
    Opcode.CONDITIONAL:'#FFE0F6',  # soft magenta
    Opcode.EXIT:       '#CCCCCC',  # soft gray
}
>>>>>>> Stashed changes


# Front End parser: parse User input prompt.txt file markers
# ToDo: rensme to FE_MARKERS
<<<<<<< Updated upstream
FE_MARKERS = [    "/TEMPLATE",      # 1
                  "/PROMPT",        # 2
                  "/DOCS",          # 4
                  "/RUN",           # 4
                  "/DEBUG_LOOP", 
                  "/EXIT"]    # 3 Lowered into a conditional loop 
=======
FE_MARKERS = [    "/TEMPLATE",      # 1 Specify dir with files to seed code folder
                  "/PROMPT",        # 2 Specify LLM call
                  "/DOCS",          # 3 Specify dir with read only docs
                  "/RUN",           # 4 Specify CLI call
                  "/DEBUG_LOOP",    # 5 Lowered into a conditional loop 
                  "/EXIT"]          # 6 
>>>>>>> Stashed changes

# Markers within a node after the IR_MARKER parsing, that trigger second order effects
INTRA_NODE_MARKERS = ["/RO"]

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
        
        contents['id'] = self.node_counter

        self.graph.add_node(node_name, opcode=opcode, contents=contents)
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
        
        iteration_count = cond_contents.get('iteration_count', 0)
        iteration_max = cond_contents.get('iteration_max', 3)
        if iteration_count >= iteration_max:
            raise ValueError(f"Conditional iteration limit reached: {iteration_count}/{iteration_max}")

        # Increment the iteration count
        cond_contents['iteration_count'] = iteration_count + 1
        
        cond_result = cond_contents.get('condition', False)
        logger.info(f"Conditional result: {cond_result}")
        if cond_result:
            queue.append(cond_contents['true_node_target'])
        else:
            queue.append(cond_contents['false_node_target'])
            
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
    Draw a directed control flow graph using networkx and matplotlib, with a custom layer-based layout.
    Back-edges (loops) are routed with right-angle (bar) arrows with armA=20, armB=20 for clean horizontal routing on the right.
    """
    plt.figure(figsize=(30, 30))
    pos = _layered_layout(graph, y_spacing=0.22, x_spacing=0.55)
    fig, ax = plt.subplots(figsize=(30, 30))

    # Compute layers for all nodes
    entry_nodes = [n for n in graph.nodes() if graph.in_degree(n) == 0]
    if not entry_nodes:
        entry_nodes = [list(graph.nodes())[0]]
    layer = {}
    for node in graph.nodes():
        max_len = 0
        for entry in entry_nodes:
            try:
                for path in nx.all_simple_paths(graph, entry, node):
                    max_len = max(max_len, len(path)-1)
            except Exception:
                continue
        layer[node] = max_len

    # Identify back-edges (edges going up in the flow)
    back_edges = []
    normal_edges = []
    for u, v in graph.edges():
        if layer[v] < layer[u]:
            back_edges.append((u, v))
        else:
            normal_edges.append((u, v))

    # Draw normal edges first
    edge_labels = {}
    for u, v in normal_edges:
        u_opcode = graph.nodes[u]['opcode']
        if u_opcode == Opcode.CONDITIONAL:
            cond = graph.nodes[u]['contents']
            if 'true_node_target' in cond and v == cond['true_node_target']:
                edge_labels[(u, v)] = 'True'
            elif 'false_node_target' in cond and v == cond['false_node_target']:
                edge_labels[(u, v)] = 'False'
    nx.draw_networkx_edges(graph, pos, edgelist=normal_edges, ax=ax, arrows=True, arrowstyle='-|>',
                          arrowsize=25, width=2, edge_color='black',
                          connectionstyle='arc3,rad=0.1')
    if edge_labels:
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels,
                                    font_color='red', font_size=11, ax=ax)

    # Draw nodes with different shapes and content
    node_labels = {}
    for node in graph.nodes():
        opcode = graph.nodes[node]['opcode']
        contents = graph.nodes[node]['contents']
        # Create label with content
        if opcode == Opcode.PROMPT and 'prompt' in contents:
            prompt = contents['prompt']
            if len(prompt) > 50:
                prompt = prompt[:47] + "..."
            label = f"{node}\n{prompt}"
        elif opcode == Opcode.RUN and 'command' in contents:
            command = contents['command']
            if len(command) > 50:
                command = command[:47] + "..."
            label = f"{node}\n{command}"
        else:
            label = node
        node_labels[node] = label
        x, y = pos[node]
        color = OPCODE_COLORS[opcode]
        # Draw node with appropriate shape
        if opcode == Opcode.CONDITIONAL:
            width = 0.156
            height = 0.08
            diamond = Polygon([
                (x, y+height), (x+width, y), (x, y-height), (x-width, y)
            ], closed=True, facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(diamond)
        elif opcode == Opcode.EXIT:
            circle = Circle((x, y), 0.11, facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(circle)
        else:
            rect = FancyBboxPatch((x-0.18, y-0.055), 0.36, 0.11,
                                 boxstyle="round,pad=0.02",
                                 facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(rect)
    # Draw labels
    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=9,
                           font_weight='bold', ax=ax, verticalalignment='center')

    # Draw custom back-edges (right-angle bar connection style with armA=20, armB=20)
    for u, v in back_edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        # Start at right side of u
        start = (x0 + 0.18, y0)
        end = (x1 + 0.18, y1)
        # Use bar connection style for right-angle with arms
        arrow = FancyArrowPatch(start, end, connectionstyle=f'arc,angleA=0,angleB=0,armA={0.1},armB={0.1}',
                                arrowstyle='-|>', mutation_scale=0, linewidth=2, color='black', zorder=10)
        ax.add_patch(arrow)

    plt.title("Control Flow Graph", size=20, fontweight='bold')
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.2, 1.2)
    ax.axis('off')
    plt.savefig(os.path.join(file_path, file_name), dpi=300, bbox_inches='tight')
    plt.close()

def _layered_layout(graph: nx.DiGraph, y_spacing=0.22, x_spacing=0.55) -> dict:
    """
    Assign each node a vertical layer based on the longest path from the entry node.
    Nodes in the same layer are spread horizontally, with adjustable spacing.
    """
    entry_nodes = [n for n in graph.nodes() if graph.in_degree(n) == 0]
    if not entry_nodes:
        entry_nodes = [list(graph.nodes())[0]]
    layer = {}
    for node in graph.nodes():
        max_len = 0
        for entry in entry_nodes:
            try:
                for path in nx.all_simple_paths(graph, entry, node):
                    max_len = max(max_len, len(path)-1)
            except nx.NetworkXNoPath:
                continue
        layer[node] = max_len
    layers = {}
    for node, l in layer.items():
        layers.setdefault(l, []).append(node)
    sorted_layers = sorted(layers.items())
    pos = {}
    total_layers = len(sorted_layers)
    for i, (l, nodes_in_layer) in enumerate(sorted_layers):
        y = 1.0 - (i * y_spacing)
        n_nodes = len(nodes_in_layer)
        if n_nodes == 1:
            xs = [0.5]
        else:
            xs = [0.5 + (j - (n_nodes-1)/2) * x_spacing for j in range(n_nodes)]
        for x, node in zip(xs, nodes_in_layer):
            pos[node] = (x, y)
    for node in graph.nodes():
        if node not in pos:
            pos[node] = (0.5, -0.1)
    return pos

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
    node_name_0 = opcode(operand1, operand2) {contents} [id: X]
    node_name_1 = opcode(operand1, operand2) {contents} [id: Y]
    
    ... 
    """

    graph_string = "\n"
    for node in graph.nodes():
        # Get node attributes
        node_data = graph.nodes[node]
        opcode = node_data.get('opcode', 'UNKNOWN')
        contents = node_data.get('contents', '')
        node_id = node_data.get('id', 'UNKNOWN')
        
        # Get operands (successors of the node)
        operands = list(graph.predecessors(node))
        
        # Format and print the node information
        operands_str = ', '.join(str(op) for op in operands)
        if verbose:
            graph_string += f"{node} = {opcode}({operands_str}) {{{contents}}} [id: {node_id}]\n"
        else:
            graph_string += f"{node} = {opcode}({operands_str})\n"
    
    return graph_string
    


