import os
import shutil
from pathlib import Path
from typing import Tuple    

def create_symlink_safely(target: str, link_path: str):
    """
    Create a symlink safely with cross-platform support.
    
    Args:
        target: The target path to link to
        link_path: The path where the symlink should be created
    """
    try:
        # Remove existing link if it exists
        if os.path.exists(link_path):
            if os.path.islink(link_path):
                os.unlink(link_path)
            else:
                shutil.rmtree(link_path)
        
        # Create a relative symlink for better VSCode compatibility
        target_path = Path(target)
        link_path_obj = Path(link_path)
        relative_target = os.path.relpath(target_path, link_path_obj.parent)
        
        # Create the symlink with relative path
        os.symlink(relative_target, link_path)
        return True
    except OSError as e:
        print(f"Warning: Could not create symlink {link_path} -> {target}: {e}")
        # Fallback: create a regular directory and copy contents
        print("Falling back to directory copy...")
        shutil.copytree(target, link_path, dirs_exist_ok=True)
        return False

def setup_project_directories(output_dir: str, project_name: str) -> Tuple[str, str, str, str]:
    """
    Set up project directories for replay and code storage.
    
    Args:
        output_dir (str): Base output directory path
        project_name (str): Name of the project
        
    Returns:
        Tuple[str, str]: Paths to replay and code directories
        
    Raises:
        FileNotFoundError: If output_dir doesn't exist


    Example directory structure in the output_dir:
    replay_output/                  <--- output_dir
        project_dir/                <--- project_dir
            1 /                     # First run
                code/
                read_only/
                replay/
                    replay_state.json
                    epic.png
                    epic.txt
                    run_tests_pass_fail.txt
            2 /                     # Second run  
                code/
                read_only/
                replay/
                    replay_state.json
                    epic.png
                    epic.txt
                    run_tests_pass_fail.txt
        latest -> 2/                <--- symlink to latest run directory
        replay/
            replay_counter.txt
    """
    
    # =======================================================
    #                 Replay Output Directory Setup
    # =======================================================
    
    # Check if output_dir exists
    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output directory {output_dir} does not exist")
    
    # =======================================================
    #                 Epic Output Directory Setup
    # =======================================================

    # Create project directory if it doesn't exist
    project_dir = os.path.join(output_dir, project_name)
    
    
    # Set up a new project directory
    if not os.path.exists(project_dir):
        print(f"Project directory {project_dir} does not exist. Creating it now...")
        os.makedirs(project_dir, exist_ok=True)

        # Create replay master directory
        replay_master_dir = os.path.join(project_dir, "replay")
        os.makedirs(replay_master_dir, exist_ok=False)
        
        # Note: latest/ directory will be created as a symlink in post_replay_dir_cleanup
        latest_dir = os.path.join(project_dir, "latest")

        # New replay_counter.txt
        counter_file = os.path.join(replay_master_dir, "replay_counter.txt")
        with open(counter_file, "w") as f:
            f.write("0")
        current_count = 0
    else:
        # Target an existing project directory
        replay_master_dir = os.path.join(project_dir, "replay")
        counter_file = os.path.join(replay_master_dir, "replay_counter.txt")
        latest_dir = os.path.join(project_dir, "latest")

        # Read current counter value
        with open(counter_file, "r") as f:
            current_count = int(f.read().strip())
        
        # Increment counter
        with open(counter_file, "w") as f:
            f.write(str(current_count + 1))
        

    # =======================================================
    #        Creation of epic_dir
    # =======================================================

    # Create new replay directory with incremented number
    epic_dir = os.path.join(project_dir, str(current_count + 1))
    os.makedirs(epic_dir, exist_ok=True)
    
    # Create replay and code subdirectories
    replay_dir = os.path.join(epic_dir, "replay")
    code_dir = os.path.join(epic_dir, "code")
    os.makedirs(replay_dir, exist_ok=True)
    os.makedirs(code_dir, exist_ok=True)
    
    return code_dir, replay_dir, project_dir, latest_dir, epic_dir
    

def post_replay_dir_cleanup(project_dir: str, latest_dir: str, epic_dir: str):
    """
    This function is called after the replay directory is created.
    It will create/update a symlink from latest/ to the most recent epic directory.
    """
    print("\n\nDir post processing:")
    
    create_symlink_safely(epic_dir, latest_dir)    
    
    