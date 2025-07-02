import networkx as nx
import logging
from typing import List

from .ir.ir import EpicIR, Opcode

<<<<<<< Updated upstream

=======
def get_run_exit_code(run_node) -> str:
    """
    Get the file path for the command exit code.
    """
    # Get the "command_result_file" from node contents
    exit_code = run_node.get('contents', {}).get('exit_code', None)
    if exit_code is None:
        raise ValueError(f"Command exit code not found for node: {run_node}. Command did run not or failed.")
    
    return exit_code

# type: "stdout" or "stderr"
def get_run_log(run_node, type: str) -> str:
    """
    Get the file path for the run log.
    """
    # Get the "command_result_file" from node contents
    run_log_file_path = run_node.get('contents', {}).get(f"{type}_file", None)
    return run_log_file_path

# Runs a command
# If it succeeds, exit
# If it fails, run a fix-it chain
#   The first prompt in the fix-it chain runs a command to investigate the issue
#   The second prompt in the fix-it chain runs a command to fix the issue.
#   After this we go back to run the original command and repeat the process 
#   till we fix the issue or hit the iteration limit.
>>>>>>> Stashed changes
def pass_lower_debug_loop(epic: EpicIR) -> EpicIR:
    print("\n\nPASS: Lower Debug Loop")

    # Find DEBUG_LOOP node, support lowering only one. 
    debug_loop_node = None
    debug_loop_node_id = None
    found = 0
    for node_id in epic.graph.nodes():
        if epic.graph.nodes[node_id]['opcode'] == Opcode.DEBUG_LOOP:
            debug_loop_node = epic.graph.nodes[node_id]
            debug_loop_node_id = node_id
            found += 1
    
    if(found > 1):
        logger.error(f"Multiple DEBUG_LOOP nodes found: {found}. Only one is supported for now.")
        return epic

    if debug_loop_node is None:
        print("No DEBUG_LOOP node found")
        return epic
    
    #print(f"DEBUG_LOOP node found: {debug_loop_node['id']}")
    debug_loop_node_command = debug_loop_node.get('contents', {}).get('command', None)
    if debug_loop_node_command is None:
        raise ValueError(f"Command not found for DEBUG_LOOP node: {debug_loop_node}")
    else:
        print(f"DEBUG_LOOP node command: {debug_loop_node_command}")

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
                                    "iteration_max":   3, # runtime
                                    "condition": False,   # runtime
                                    })
    

    # ----- Make a FixIt node -----
    # To be expanded into 2 prompts:
    # Prompt 1: Review the error log and idenfity files that need to be fixed.
    # Prompt 2: Fix the files
    def get_fix_it_prompt(run_node) -> str:
        run_stderr_file_path = get_run_log(run_node, "stderr")
        if(run_stderr_file_path is None):
            logger.warning(f"Run node {run_node} has no stderr file path")
        
        return         

    # read file content client_instructions_indentify_issue.txt from replay folder
    loop_prompt_investigate_node = epic.add_node(opcode=Opcode.PROMPT, 
    contents={"prompt": "Analyze the error log at @run_logs:{run_stderr_file_path} and identify what must be fixed.",
              "type": "investigation"})
    
    loop_prompt_informed_fixnode = epic.add_node(opcode=Opcode.PROMPT, contents={
        "prompt": "You identified that @code:{path_to_fix} needs to be fixed @include_response",
        "include_response": loop_prompt_investigate_node})
        
    # Add edges for DEBUG_LOOP node
    epic.graph.add_edge(debug_loop_predecessor, run_check_node)    
    
    # Add edges for CONDITIONAL node
    epic.graph.add_edge(run_check_node, conditional_node)  # input to conditional
        
    # Connect the conditional flow:
    # If condition is true (worked): go to debug_loop_user (exit)
    # If condition is false (not worked): go to loop_prompt (fix it)
    epic.graph.add_edge(conditional_node, debug_loop_successor)  # true path - exit
    epic.graph.add_edge(conditional_node, loop_prompt_investigate_node) # false path - fix it
    
    # Connect the fix-it loop
    epic.graph.add_edge(loop_prompt_investigate_node, loop_prompt_informed_fixnode)
    epic.graph.add_edge(loop_prompt_informed_fixnode, run_check_node)
    epic.graph.add_edge(run_check_node, conditional_node)  # back to conditional to check again
    
    # Set the conditional node targets
    epic.graph.nodes[conditional_node]['contents']['true_node_target'] = debug_loop_successor

    epic.graph.nodes[conditional_node]['contents']['false_node_target'] = loop_prompt_investigate_node

   
    
    

    return epic
