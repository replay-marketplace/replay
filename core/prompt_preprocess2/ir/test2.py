import networkx as nx
  

import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes with some attributes
G.add_node("A", label="Start", color="lightgreen")
G.add_node("B", label="Process", color="lightblue") 
G.add_node("C", label="End", color="lightcoral")
G.add_node("D", label="Data", color="lightyellow")
G.add_node("E", label="Analysis", color="lightpink")
G.add_node("F", label="Storage", color="lightgray")
G.add_node("G", label="Output", color="lightsalmon")
G.add_node("H", label="Review", color="lightcyan")

# Add edges to connect the nodes
G.add_edge("A", "B", weight=1)
G.add_edge("B", "C", weight=2)
G.add_edge("A", "C", weight=3)  # Direct path from A to C
G.add_edge("B", "D", weight=2)  # Process to Data
G.add_edge("D", "E", weight=1)  # Data to Analysis
G.add_edge("E", "F", weight=2)  # Analysis to Storage
G.add_edge("F", "G", weight=1)  # Storage to Output
G.add_edge("G", "H", weight=1)  # Output to Review
G.add_edge("H", "C", weight=2)  # Review to End
G.add_edge("E", "B", weight=1)  # Analysis back to Process

# Create the visualization
plt.figure(figsize=(10, 6))

# Define positions for the nodes
pos = nx.spring_layout(G, seed=42)  # seed for consistent layout

# Get node colors from attributes
node_colors = [G.nodes[node]['color'] for node in G.nodes()]

# Draw the graph
nx.draw(G, pos, 
        with_labels=True,           # Show node labels
        node_color=node_colors,     # Use custom colors
        node_size=2000,             # Make nodes bigger
        font_size=16,               # Larger font
        font_weight='bold',         # Bold text
        arrows=True,                # Show arrow direction
        arrowsize=20,               # Bigger arrows
        edge_color='gray',          # Edge color
        width=2)                    # Edge thickness

# Add edge labels (weights)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=12)

# Add a title
plt.title("Simple 3-Node Directed Graph", size=16, weight='bold')
plt.axis('off')  # Turn off axis
plt.tight_layout()

# Save the graph to a file
plt.savefig('graph_visualization.png', dpi=300, bbox_inches='tight')

# Print some information about the graph
print("Graph Information:")
print(f"Nodes: {list(G.nodes())}")
print(f"Edges: {list(G.edges())}")
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

# Print node attributes
print("\nNode Attributes:")
for node, attrs in G.nodes(data=True):
    print(f"Node {node}: {attrs}")

# Print edge attributes  
print("\nEdge Attributes:")
for edge in G.edges(data=True):
    print(f"Edge {edge[0]} -> {edge[1]}: weight = {edge[2]['weight']}")

