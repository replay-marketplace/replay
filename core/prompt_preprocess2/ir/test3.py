import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum
import matplotlib.colors as mcolors

# Print all available named colors
print("Available named colors:")
for color_name in mcolors.get_named_colors_mapping():
    print(color_name)

class Opcode(Enum):
    READ_ONLY = "ro"
    PROMPT = "prompt"
    COMMAND = "command"
    TEMPLATE = "template"

# Create a directed graph
G = nx.DiGraph()

# Add nodes with some attributes
G.add_node("sw_template", opcode=Opcode.TEMPLATE, contents={"path": "path/my_project/"})
G.add_node("prompt1", opcode=Opcode.PROMPT, contents={"prompt": "bla bla bla"})
G.add_node("prompt2", opcode=Opcode.PROMPT, contents={"prompt": "bla bla bla"})
G.add_node("prompt3", opcode=Opcode.PROMPT, contents={"prompt": "bla bla bla"})
G.add_node("ro1", opcode=Opcode.READ_ONLY, contents={"path": "path/file.txt"})

# Add edges
G.add_edge("sw_template", "prompt1")
G.add_edge("prompt1", "prompt2")
G.add_edge("prompt2", "prompt3")
G.add_edge("ro1", "prompt2")

# Create the figure
plt.figure(figsize=(8, 10))  # Adjusted figure size for vertical layout

# Use kamada_kawai_layout which is better for hierarchical structures
pos = nx.kamada_kawai_layout(G)

# Define color mapping for opcodes
opcode_colors = {
    Opcode.READ_ONLY: 'green',
    Opcode.PROMPT: 'blue',
    Opcode.COMMAND: 'red',
    Opcode.TEMPLATE: 'red'
}

# Create a list of colors for each node based on its opcode
node_colors = [opcode_colors[G.nodes[node]['opcode']] for node in G.nodes()]

# Draw the graph
nx.draw(G, pos, with_labels=True, node_color=node_colors,
        node_size=2000, arrowsize=20, font_size=10)

# Add a title
plt.title("Vertical Tree Layout", size=16, weight='bold')
plt.axis('off')  # Turn off axis

# Save the graph to a file
plt.savefig('graph_visualization.png', dpi=300, bbox_inches='tight')
plt.close()  # Close the figure to free memory
