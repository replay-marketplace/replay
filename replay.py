import os
import json
import anthropic
import networkx as nx
import shutil
import subprocess

from pathlib import Path
from core.dir_preprocessing import setup_project_directories
from core.prompt_preprocess2.processor3 import prompt_preprocess3
from core.json_to_code.json_to_code import json_to_code
from core.prompt_preprocess2.ir.ir import EpicIR, Opcode
from core.code_to_json.code_to_json import code_to_json
from helpers.utils import debug_print


# ------------------------------------------------------------
# Process Opcode.TEMPLATE: copy the code into the code_dir
# ------------------------------------------------------------
def process_template_node(epic: EpicIR, node: str, code_dir: str):
    DEBUG = True
    INDENT = 2
    
    template_path = epic.graph.nodes[node]['contents']['path']
    debug_print(f"Processing template: {template_path}", INDENT, DEBUG)

    # Determine if the path exists
    if not os.path.exists(template_path):
        debug_print(f"Template file does not exist: {template_path}", INDENT, DEBUG)
        
    else:
        # Check if template_path is a file
        if os.path.isfile(template_path):
            
            # Copy the template file to the replay directory
            shutil.copy(template_path, os.path.join(code_dir, os.path.basename(template_path)))
            debug_print(f"Copied template file to code_dir directory: {os.path.join(code_dir, os.path.basename(template_path))}", INDENT, DEBUG)
        
        # Check if template_path is a directory
        elif os.path.isdir(template_path):

            # Copy the template directory to the replay directory
            shutil.copytree(template_path, os.path.join(code_dir, os.path.basename(template_path)), dirs_exist_ok=True)
            debug_print(f"Copied template directory to code_dir directory: {os.path.join(code_dir, os.path.basename(template_path))}", INDENT, DEBUG)
    
# ------------------------------------------------------------
# Process Opcode.PROMPT
# ------------------------------------------------------------ 
def process_prompt_node(client: anthropic.Anthropic, system_instructions: str, epic: EpicIR, node: str, code_dir: str, ro_dir: str, replay_dir: str):
    DEBUG = True
    INDENT = 2
    
    prompt = ""

    # Prepare the prompt text for a "loop debug prompt" node
    debug_print(f"Processing prompt: {epic.graph.nodes[node]['contents']}", INDENT, DEBUG)
    # Prepare the Prompt text, check if "terminal_output" exists
    if epic.graph.nodes[node]['contents'].get('terminal_output') is not None:
        
        # Prompt prep
        print(f"terminal_output: {epic.graph.nodes[node]['contents']['terminal_output']}")
        with open(os.path.join(replay_dir, epic.graph.nodes[node]['contents']['terminal_output']), "r") as f:
            terminal_output = f.read()
            debug_print(f"terminal_output: {terminal_output}", INDENT+2, DEBUG)
        prompt = f"Fix this error: {terminal_output}"
        debug_print(f"Processing prompt: {prompt}", INDENT, DEBUG)

        # Delete the used files in the replay_dir:
        file =  epic.graph.nodes[node]['contents']['terminal_output']
        os.remove(os.path.join(replay_dir, file))
        #file =  epic.graph.nodes[node]['contents']['terminal_output']
        #os.remove(os.path.join(replay_dir, file))


    else:
        prompt = epic.graph.nodes[node]['contents']['prompt']
        debug_print(f"Processing prompt: {prompt}", INDENT, DEBUG)

    # Step 2: Create the agent_json object (prompt, code, read_only, command_to_run)
    llm_json = {}
    llm_json['prompt'] = prompt
    llm_json['code_to_edit'] = code_to_json(code_dir)
    llm_json['read_only_files'] = code_to_json(ro_dir)
    llm_json['commands_to_run'] = []
    #llm_json['commands_to_rename_files'] = []
    #llm_json['commands_to_run_tests'] = []

    # Print the json object
    #print("\n\n\njson_object: ")
    #print(json.dumps(llm_json, indent=4))

    # Generate a string from the json object
    llm_json_str = json.dumps(llm_json, indent=4)

    # Send to Claude
    response = client.messages.create(
                    model="claude-3-7-sonnet-20250219",
                    system=system_instructions,
                    messages=[{"role": "user", "content": llm_json_str}],
                    max_tokens=4096
                    )

    # Print response
    #print(f"\n\nClaude's response: {response.content[0].text}")

    # Convert response to code
    response_json = json.loads(response.content[0].text)
    response_code = response_json['files']
    json_to_code(code_dir, response_json['files'])


def process_run_node(epic: EpicIR, node: str, code_dir: str, replay_dir: str):
    DEBUG = True
    INDENT = 2

    debug_print(f"node: {node}", INDENT, DEBUG)
    
    command_to_run = "chmod 755 run_tests.sh"
    subprocess.run(command_to_run, shell=True, cwd=code_dir)
    
    command_to_run = epic.graph.nodes[node]['contents']['command_to_run']
    debug_print(f"GOING TO RUN COMMAND: {command_to_run}", INDENT, DEBUG)
    subprocess.run(command_to_run, shell=True, cwd=code_dir)
    
    # Load file contents from ../replay/run_tests_pass_fail.txt into this node
    with open(os.path.join(replay_dir, "run_tests_pass_fail.txt"), "r") as f:
        epic.graph.nodes[node]['contents']['passed'] = f.read()
    
    debug_print(f"Test results: {epic.graph.nodes[node]['contents']['passed']}", INDENT, DEBUG)
    

def replay(input_prompt_file: str, project_name: str, output_dir: str = "replay_output"):
    DEBUG = True
    INDENT = 0
    
    # =======================================================
    #                   ONE TIME SETUP
    # =======================================================
    
    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    # Initialize Anthropic client
    client = anthropic.Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"]
    )
    
    # Load and setup system instructions
    with open("input_const/client_instructions_with_json.txt", "r") as f:
        system_instructions = f.read()

    # Setup project directories
    code_dir, replay_dir, ro_dir = setup_project_directories(output_dir, project_name)
    #print("output_dir: ", output_dir)
    #print("code_dir: ", code_dir)
    #print("replay_dir: ", replay_dir)
    #print("ro_dir: ", ro_dir)

    # Preprocess the input prompt & copy input prompt to replay directory
    epic = prompt_preprocess3(input_prompt_file, replay_dir)
    
    # =======================================================
    #                   RUNTIME: REPLAY LOOP
    # =======================================================
    print("\n\n")
    print("=======================================================================")
    print("=======================================================================")
    print("                        RUNTIME: REPLAY LOOP")
    print("=======================================================================")
    print("=======================================================================")
    print("\n\n")

    # DFS traversal of the networkx graphd
    dfs_nodes = list(nx.dfs_preorder_nodes(epic.graph, epic.first_node))
    print("dfs_nodes: ", dfs_nodes)
    
    # Loop over nodes
    for node in dfs_nodes:
        
        if epic.graph.nodes[node]['opcode'] == Opcode.TEMPLATE:
            debug_print("\n\n--- RUNTIME: start template: ---- ", INDENT, DEBUG)
            process_template_node(epic, node, code_dir)
            debug_print("--- template: END ----", INDENT, DEBUG)                                
        
        elif epic.graph.nodes[node]['opcode'] == Opcode.PROMPT:
            debug_print("\n\n--- RUNTIME: start prompt:  ---- ", INDENT, DEBUG)
            process_prompt_node(client, system_instructions, epic, node, code_dir, ro_dir, replay_dir)
            debug_print("--- prompt: END ----", INDENT, DEBUG)  

        elif epic.graph.nodes[node]['opcode'] == Opcode.RUN:
            debug_print("\n\n--- RUNTIME: start run ---- ", INDENT, DEBUG)
            process_run_node(epic, node, code_dir, replay_dir)
            debug_print("--- run: END ----", INDENT, DEBUG) 

        input("Press Enter to continue...")     
        
    print("\n\n\nDone with replay loop\n\n\n")

    

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Process input prompts and generate code using Claude AI')
    parser.add_argument('input_prompt_file', help='Path to the input prompt file')
    parser.add_argument('project_name', help='Name of the project')
    
    
    args = parser.parse_args()
    
    replay(args.input_prompt_file, args.project_name)
