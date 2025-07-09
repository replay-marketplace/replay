import networkx as nx
import logging
from typing import List

from ..ir.ir import EpicIR, Opcode

def get_run_exit_code(run_node: dict) -> str:
    """
    Extract the exit code from a RUN node.
    
    Args:
        run_node (dict): The RUN node containing execution results
        
    Returns:
        str: The exit code from the command execution
        
    Raises:
        ValueError: If the exit code is not found in the node contents
    """
    # Get the "command_result_file" from node contents
    exit_code = run_node.get('contents', {}).get('exit_code', None)
    if exit_code is None:
        raise ValueError(f"Command exit code not found for node: {run_node}. Command did run not or failed.")
    
    return exit_code

def get_run_log(run_node: dict, type: str) -> str:
    """
    Extract the log file path from a RUN node.
    
    Args:
        run_node (dict): The RUN node containing execution results
        type (str): The type of log to retrieve ("stdout" or "stderr")
        
    Returns:
        str: The file path for the requested log type, or None if not found
    """
    # Get the "command_result_file" from node contents
    run_log_file_path = run_node.get('contents', {}).get(f"{type}_file", None)
    return run_log_file_path


def pass_lower_debug_loop(epic: EpicIR) -> EpicIR:
    """
    Lower DEBUG_LOOP nodes into a retry loop with fix mechanism.
    """

    while True:
        debug_loop_node, debug_loop_node_id = find_first_debug_loop_node(epic)
        if debug_loop_node is None:
            break
        replace_debug_loop_node(epic, debug_loop_node, debug_loop_node_id)
    
    return epic


def find_first_debug_loop_node(epic: EpicIR) -> tuple[dict, str]:    
    """
    Returns:
        tuple[dict, str]: A tuple containing the DEBUG_LOOP node and its ID, or None if not found
    """
    debug_loop_node = None
    debug_loop_node_id = None

    for node_id in epic.graph.nodes():
        if epic.graph.nodes[node_id]['opcode'] == Opcode.DEBUG_LOOP:
            debug_loop_node = epic.graph.nodes[node_id]
            debug_loop_node_id = node_id
            break;

    return debug_loop_node, debug_loop_node_id

def replace_debug_loop_node(epic: EpicIR, debug_loop_node: dict, debug_loop_node_id: str):
    """
    This pass transforms high-level DEBUG_LOOP nodes into a concrete implementation
    that repeatedly runs a command until it succeeds or hits an iteration limit.
    The lowering creates:
    
    1. A RUN node to execute the command
    2. A CONDITIONAL node to check success/failure
    3. A FIX node to analyze failures and suggest fixes
    4. Control flow edges to create the retry loop
    
    Flow pattern:
    ```
    [previous] -> RUN -> CONDITIONAL -> [success_target]
                           |
                           v (on failure)
                         FIX -> (back to RUN)
    ```
    
    The DEBUG_LOOP node contains:
    - command: The shell command to execute repeatedly
    
    The generated structure includes:
    - RUN node: Executes the command and captures results
    - CONDITIONAL node: Checks exit code and manages iteration count
    - FIX node: Analyzes failures and applies corrections
    
    Args:
        epic (EpicIR): The intermediate representation graph to transform
        
    Returns:
        EpicIR: The modified graph with DEBUG_LOOP nodes lowered
        
    Raises:
        ValueError: If multiple DEBUG_LOOP nodes found (only one supported)
        ValueError: If command not found in DEBUG_LOOP node
        ValueError: If DEBUG_LOOP node has multiple predecessors/successors
    
    Note:
        Currently supports lowering only one DEBUG_LOOP node per graph.
        The iteration limit is hardcoded to 5 attempts.
    """
    
    debug_loop_node_command = debug_loop_node.get('contents', {}).get('command', None)
    if debug_loop_node_command is None:
        raise ValueError(f"Command not found for DEBUG_LOOP node: {debug_loop_node}")
    else:
        print(f"Command: \n\t{debug_loop_node_command}")

    # Delete the DEBUG_LOOP node
    debug_loop_predecessors = list(epic.graph.predecessors(debug_loop_node_id))
    debug_loop_successors = list(epic.graph.successors(debug_loop_node_id))
    
    epic.graph.remove_node(debug_loop_node_id)
    print(f"debug_loop_predecessors: {debug_loop_predecessors}")
    print(f"debug_loop_successors: {debug_loop_successors}")
    
    # Get Operands & Users
    debug_loop_predecessor = debug_loop_predecessors[0]  
    debug_loop_successor = debug_loop_successors[0]
    if (len(debug_loop_predecessors) > 1 or len(debug_loop_successors) > 1):
        raise ValueError(f"Taking a single predecessor and successor for the debug loop {debug_loop_node_command}" )

    # ----- Make a a RUN node -----    
    run_check_node = epic.add_node(opcode=Opcode.RUN, contents={"command": debug_loop_node_command})        

    # ----- Make a a CONDITIONAL node -----
    # Create a new node with the same contents as the DEBUG_LOOP node    
    conditional_node = epic.add_node(opcode=Opcode.CONDITIONAL, 
                         contents={"iteration_count": 0,                                      
                                    "run_node_id": run_check_node,
                                    "true_node_target": "",
                                    "false_node_target": "",
                                    "iteration_max":   5, # runtime
                                    "condition": False,   # runtime
                                    })
    

    # ----- Make a FIX node -----
    # This will analyze the RUN node's logs and suggest fixes
    fix_node = epic.add_node(opcode=Opcode.FIX, 
                            contents={"run_ref": run_check_node})
        
    # Add edges for DEBUG_LOOP node
    epic.graph.add_edge(debug_loop_predecessor, run_check_node)    
    
    # Add edges for CONDITIONAL node
    epic.graph.add_edge(run_check_node, conditional_node)  # input to conditional
        
    # Connect the conditional flow:
    # If condition is true (worked): go to debug_loop_user (exit)
    # If condition is false (not worked): go to fix_node (fix it)
    epic.graph.add_edge(conditional_node, debug_loop_successor)  # true path - exit
    epic.graph.add_edge(conditional_node, fix_node) # false path - fix it
    
    # Connect the fix loop back to the run node
    epic.graph.add_edge(fix_node, run_check_node)
    
    # Set the conditional node targets
    epic.graph.nodes[conditional_node]['contents']['true_node_target'] = debug_loop_successor
    epic.graph.nodes[conditional_node]['contents']['false_node_target'] = fix_node

    return epic
