import networkx as nx
import matplotlib.pyplot as plt
import os
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrowPatch
from .ir import Opcode


OPCODE_COLORS = {
    Opcode.TEMPLATE:   '#FFB3BA',  # soft pink
    Opcode.PROMPT:     '#BAE1FF',  # soft blue
    Opcode.READ_ONLY:  '#BFFCC6',  # soft green
    Opcode.DOCS:       '#FFFFBA',  # soft yellow
    Opcode.RUN:        '#D5BAFF',  # soft lavender
    Opcode.DEBUG_LOOP: '#FFDFBA',  # soft orange
    Opcode.CONDITIONAL:'#FFE0F6',  # soft magenta
    Opcode.FIX:        '#FFB366',  # soft orange-red
    Opcode.EXIT:       '#CCCCCC',  # soft gray    
}


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
            rect = FancyBboxPatch((x-0.08, y-0.055), 0.16, 0.11,
                                 boxstyle="round,pad=0.02",
                                 facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(rect)
    # Draw labels
    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=12,
                           font_weight='bold', ax=ax, verticalalignment='center')

    # Draw back-edges with bracket-like connection style from right border to right border
    if back_edges:
        # Create custom positions for back edges that start and end at right borders
        back_edge_pos = {}
        for u, v in back_edges:
            x_u, y_u = pos[u]
            x_v, y_v = pos[v]
            # Start at right border of source node (x + 0.08 for the new narrower width)
            back_edge_pos[u] = (x_u + 0.1, y_u)
            # End at right border of target node
            back_edge_pos[v] = (x_v + 0.1, y_v)
        
        # Draw back edges using custom positions
        for u, v in back_edges:
            start_pos = back_edge_pos[u]
            end_pos = back_edge_pos[v]
            arrow = FancyArrowPatch(start_pos, end_pos, 
                                  connectionstyle='arc,armA=2,armB=0.2,angleA=90,angleB=90,rad=0.2',
                                  arrowstyle='-|>', linewidth=2, 
                                  color='black', zorder=-2)
            ax.add_patch(arrow)


    # Calculate canvas limits based on node positions with padding
    if pos:
        x_coords = [coord[0] for coord in pos.values()]
        y_coords = [coord[1] for coord in pos.values()]
        
        # Add padding for node sizes and labels
        x_padding = 0.25  # Account for node width (0.16) + some extra space
        y_padding = 0.2  # Account for node height and labels
        
        x_min, x_max = min(x_coords) - x_padding, max(x_coords) + x_padding
        y_min, y_max = min(y_coords) - y_padding, max(y_coords) + y_padding
        
        # Ensure minimum canvas size
        canvas_width = max(x_max - x_min, 1.0)
        canvas_height = max(y_max - y_min, 1.0)
        
        # Center the canvas if it's too small
        if canvas_width < 1.0:
            center_x = (x_min + x_max) / 2
            x_min = center_x - 0.5
            x_max = center_x + 0.5
        if canvas_height < 1.0:
            center_y = (y_min + y_max) / 2
            y_min = center_y - 0.5
            y_max = center_y + 0.5
    else:
        # Fallback if no positions
        x_min, x_max = -0.5, 1.5
        y_min, y_max = -0.2, 1.2

    plt.title("Control Flow Graph", size=20, fontweight='bold')
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.axis('off')
    ax.set_aspect('equal')  # Ensure circles stay circular
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
    node_name_0 = opcode(operand1, operand2) {contents} # [id: X]
    node_name_1 = opcode(operand1, operand2) {contents} # [id: Y]
    
    ... 
    """

    graph_string = "\n"
    for node_name in graph.nodes():
        # Get node attributes
        node = graph.nodes[node_name]
        opcode = node.get('opcode', 'UNKNOWN')
        contents = node.get('contents', '')
        node_id = node.get('id', 'UNKNOWN')
        
        # Get operands (successors of the node)
        operands = list(graph.predecessors(node_name))
        
        # Format and print the node information
        operands_str = ', '.join(str(op) for op in operands)
        if verbose:
            graph_string += f"{node_name} = {opcode}({operands_str}) {{{contents}}} # [id: {node_id}]\n"
        else:
            graph_string += f"{node_name} = {opcode}({operands_str})\n"
    
    return graph_string 