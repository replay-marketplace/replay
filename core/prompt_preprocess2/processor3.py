import shutil
import networkx as nx
from typing import List

from .parse_prompt import extract_template
from .parse_prompt import extract_next_word_after_marker
from .parse_prompt import get_string_from_file

from .ir.ir import Opcode, FE_MARKERS, INTRA_NODE_MARKERS
from .ir.ir import nx_draw_graph, Opcode, print_graph, print_graph_to_file, EpicIR

from .passes import pass_insert_exit_node
from .pass_build_graph import pass_build_epic_graph
from .pass_lower_debug_loop import pass_lower_debug_loop
from .pass_lower_prompt_file_refs import pass_lower_prompt_file_refs

def prompt_preprocess3(input_file: str, replay_dir: str) -> EpicIR:
    #print(f"Input file: {input_file}")
    #print(f"Output directory: {replay_dir}")
    
    shutil.copy(input_file, replay_dir) # Copy input_file into replay_dir
    
    epic = pass_build_epic_graph(input_file)
    print_graph(epic.graph, True)

    epic = pass_insert_exit_node(epic)
    print_graph(epic.graph, True)

    epic = pass_lower_debug_loop(epic)
    print_graph(epic.graph, True)

    epic = pass_lower_prompt_file_refs(epic)
    print_graph(epic.graph, True)

    # Print the nx graph to terminal
    print_graph(epic.graph)
    
    # ------------------------------------------------------------------------
    # Step 2 - Parse /RO
    # ------------------------------------------------------------------------
    # Loop over prompts and parse /RO
    #print("\n\nExtract RO")

    # Loop over nodes in NetworkX graph and print them
    offline_node_list = []
    for node in epic.graph.nodes():
        offline_node_list.append(node)

    ro_count = 0

    for node in offline_node_list:

        # If node opcode is Opcode.PROMPT, print the prompt
        if epic.graph.nodes[node]['opcode'] == Opcode.PROMPT:
        
            prompt = epic.graph.nodes[node]['contents']['prompt']

            # Extract all RO words from the prompt
            ro_list = extract_next_word_after_marker(prompt, "/RO")
            #print("\n\nRO list:")
            #print(ro_list)

            for ro in ro_list:
                if ro != "":
                    node_ro = f"ro_{ro_count}"
                    ro_count += 1
                    #epic.add_node(node_ro, Opcode.READ_ONLY, contents={"path": ro})
                    epic.graph.add_node(node_ro, opcode=Opcode.READ_ONLY, contents={"path": ro})

                    # Add an edge from the node_ro to the node_prompt
                    epic.graph.add_edge(node_ro, node)

                    # Store the RO folder path in the prompt node's contents
                    epic.graph.nodes[node]['contents']['ro_folder'] = ro
        
    
    nx_draw_graph(epic.graph, replay_dir, "epic.png")
    print()
    print()
    print("----------------------------------------------------------------")
    print("         PROMPT PREPROCESS 3 : FINAL GRAPH            ")
    print("----------------------------------------------------------------")
    print_graph(epic.graph)
    print()
    print()
    print()
    print_graph(epic.graph, True)
    print_graph_to_file(epic.graph, replay_dir, "epic.txt", True)


    return epic