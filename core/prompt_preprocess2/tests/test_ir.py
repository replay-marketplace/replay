import pytest
import os
import argparse
import networkx as nx
from prompt_preprocess2.processor3 import prompt_preprocess3
from prompt_preprocess2.ir.ir import EpicIR, Opcode, nx_draw_graph, print_graph, print_graph_to_file
from prompt_preprocess2.ir.ir import cfg_traversal_init_queue, cfg_traversal_step



def debug_print(message: str, indent: int = 0, DEBUG: bool = True):
    if DEBUG:
        print(" " * indent + message)


def test_1():
    
    print("Test 1")
    epic = EpicIR()

    node1 = "prompt_" + epic.get_next_node_counter()
    epic.graph.add_node(node1,opcode=Opcode.PROMPT, contents={})        
    
    node2 = "prompt_" + epic.get_next_node_counter()
    epic.graph.add_node(node2,opcode=Opcode.PROMPT, contents={})        
    epic.graph.add_edge(node1, node2)

    node3 = "exit_" + epic.get_next_node_counter()
    epic.graph.add_node(node3,opcode=Opcode.EXIT, contents={})        
    epic.graph.add_edge(node2, node3)   
    
    node4 = "prompt_" + epic.get_next_node_counter()
    epic.graph.add_node(node4,opcode=Opcode.PROMPT, contents={})        
    epic.graph.add_edge(node3, node4)

    print_graph(epic.graph)

    # Offline traversal mode - Data Flow Analysis
    dfs_nodes = list(nx.dfs_preorder_nodes(epic.graph, epic.first_node))
    print("dfs_nodes: ", dfs_nodes)
    for node in dfs_nodes:
        
        # EXIT node
        if epic.graph.nodes[node]['opcode'] == Opcode.EXIT:
            print(f"Node: {node}")
            break

        print(f"Node: {node}")
    return



def test_2():
    '''
    A simple tree with a conditional node
    '''
    DEBUG = True
    INDENT = 2

    debug_print("Test 2", 0, DEBUG)
    epic = EpicIR()
    
    node1 = "prompt_" + epic.get_next_node_counter()
    epic.graph.add_node(node1,opcode=Opcode.PROMPT, contents={})
    epic.first_node = node1

    node2 = "prompt_" + epic.get_next_node_counter()
    epic.graph.add_node(node2,opcode=Opcode.PROMPT, contents={})
    epic.graph.add_edge(node1, node2)
    
    node3 = "conditional_" + epic.get_next_node_counter()
    epic.graph.add_node(node3,
                        opcode=Opcode.CONDITIONAL,
                        contents={"iteration_count": 0, 
                                  "condition_file_path": "../replay/run_tests_pass_fail.txt",
                                  "condition": False,
                                  "true_node_target": "",
                                  "false_node_target": ""
                                  })
    epic.graph.add_edge(node2, node3)                              

    node4 = "prompt_" + epic.get_next_node_counter()
    epic.graph.add_node(node4,opcode=Opcode.PROMPT, contents={})
    epic.graph.add_edge(node3, node4)

    node5 = "prompt_" + epic.get_next_node_counter()
    epic.graph.add_node(node5,opcode=Opcode.PROMPT, contents={})
    epic.graph.add_edge(node3, node5)

    epic.graph.nodes[node3]['contents']['true_node_target'] = node4    
    epic.graph.nodes[node3]['contents']['false_node_target'] = node5

    print_graph(epic.graph, True)

    # Control Flow Traversal
    print("\n\nControl Flow Traversal:")
    queue = cfg_traversal_init_queue(epic)
    
    while queue:
        # Get the next node
        queue, current_node = cfg_traversal_step(epic, queue)
        
        # Process the next node
        debug_print(f"\nCurrent node: {current_node}", INDENT, DEBUG)
        debug_print(f"Queue: {queue}", INDENT+2, DEBUG)
        

def test_3():
    '''
    A simple conditional loop
    '''

    DEBUG = True
    INDENT = 2

    debug_print("Test 2", 0, DEBUG)
    epic = EpicIR()
    
    node1 = epic.add_node(Opcode.PROMPT, {})
    node2 = epic.add_node(Opcode.PROMPT, {})
    run = epic.add_node(Opcode.RUN, {})
    cond =  epic.add_node(opcode=Opcode.CONDITIONAL,
                          contents={"iteration_count": 0, 
                                    "iteration_max":   3, 
                                    "condition_file_path": "../replay/run_tests_pass_fail.txt",
                                    "condition": False,
                                    "true_node_target": "",
                                    "false_node_target": ""
                                     })
    true_exit = epic.add_node(Opcode.EXIT, {})
    false_fix_prompt = epic.add_node(Opcode.PROMPT, {}, "prompt_fix")

    # Set the target nodes for the conditional
    epic.graph.nodes[cond]['contents']['true_node_target'] = true_exit
    epic.graph.nodes[cond]['contents']['false_node_target'] = false_fix_prompt

    epic.graph.add_edge(node1, node2)
    epic.graph.add_edge(node2, run)
    epic.graph.add_edge(run, cond)
    epic.graph.add_edge(cond, true_exit)
    epic.graph.add_edge(cond, false_fix_prompt)
    epic.graph.add_edge(false_fix_prompt, cond)

    print_graph(epic.graph, True)
    
    # Control Flow Traversal
    print("\n\nControl Flow Traversal:")
    queue = cfg_traversal_init_queue(epic)
    
    while queue:
        # Get the next node
        queue, current_node = cfg_traversal_step(epic, queue)
        
        # Process the next node
        debug_print(f"\nCurrent node: {current_node}", INDENT, DEBUG)
        debug_print(f"Queue: {queue}", INDENT+2, DEBUG)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    parser = argparse.ArgumentParser(description='Test prompt preprocessing with a file')
    parser.add_argument('output_dir', help='Path to the output directory for testing')
    args = parser.parse_args()

    #test_1()
    #test_2()
    test_3()

if __name__ == "__main__":
    main()

    '''
    '''