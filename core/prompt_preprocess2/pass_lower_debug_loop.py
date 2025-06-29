import networkx as nx
import logging
from typing import List

from .ir.ir import Opcode, FE_MARKERS, INTRA_NODE_MARKERS
from .ir.ir import nx_draw_graph, Opcode, print_graph, print_graph_to_file, EpicIR
from .pass_build_graph import build_default_run_node

def pass_lower_debug_loop(epic: EpicIR) -> EpicIR:
    """Transform DEBUG_LOOP nodes into conditional loops with run nodes."""
    print("\n\nPASS: Lower Debug Loop")

    # Find DEBUG_LOOP node, support lowering only one. 
    debug_loop_node = None
    for node in epic.graph.nodes():
        if epic.graph.nodes[node]['opcode'] == Opcode.DEBUG_LOOP:
            debug_loop_node = node

    if debug_loop_node is None:
        print("No DEBUG_LOOP node found")
        return epic
    
    print(f"DEBUG_LOOP node found: {debug_loop_node}")
    
    # Get Operands & Users
    debug_loop_operand = list(epic.graph.predecessors(debug_loop_node))[0]  
    debug_loop_user = list(epic.graph.successors(debug_loop_node))[0]
    print(f"debug_loop_operand: {debug_loop_operand}")
    print(f"debug_loop_user: {debug_loop_user}")
    

    # ----- Make a a RUN node -----
    pre_run = build_default_run_node(epic)

    epic.graph.add_edge(debug_loop_operand, pre_run)

    # ----- Make a a CONDITIONAL node -----
    # Create a new node with the same contents as the DEBUG_LOOP node
    cond = epic.add_node(opcode=Opcode.CONDITIONAL, 
                         contents={"iteration_count": 0, 
                                    "iteration_max":   3, 
                                    "condition_file_path": "../replay/run_tests_pass_fail.txt",
                                    "condition": False,
                                    "true_node_target": "",
                                    "false_node_target": ""
                                     })
   
    # Add edges for CONDITIONAL node
    epic.graph.add_edge(pre_run, cond)  # input 
    epic.graph.add_edge(cond, debug_loop_user) # output
    epic.graph.nodes[cond]['contents']['true_node_target'] = debug_loop_user
    
    # Delete the DEBUG_LOOP node
    epic.graph.remove_node(debug_loop_node)

    # ----- Make a RUN node -----
    loop_prompt = epic.add_node(opcode=Opcode.PROMPT, contents={"prompt": "", "terminal_output": "run_tests_terminal_output.txt"})
    loop_run = build_default_run_node(epic)
    
    epic.graph.add_edge(cond, loop_prompt)
    epic.graph.add_edge(loop_prompt, loop_run)
    epic.graph.add_edge(loop_run, cond)

    return epic
