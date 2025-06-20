import os
from pathlib import Path
from typing import Tuple

def setup_project_directories(output_dir: str, project_name: str) -> Tuple[str, str, str]:
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
            1 /
            2 /
            3 /                     <--- epic_dir
                code/
                read_only/
                replay/ 
            replay_counter.txt
    """
    
    # =======================================================
    #                 Directory Setup
    # =======================================================
    
    # Check if output_dir exists
    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output directory {output_dir} does not exist")
    
    # Create project directory if it doesn't exist
    project_dir = os.path.join(output_dir, project_name)
    os.makedirs(project_dir, exist_ok=True)
    
    # =======================================================
    #             Handling of replay_counter.txt
    # =======================================================
    
    # Handle replay counter
    counter_file = os.path.join(project_dir, "replay_counter.txt")
    if not os.path.exists(counter_file):
        with open(counter_file, "w") as f:
            f.write("0")
    
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
    ro_dir = os.path.join(epic_dir, "read_only")
    os.makedirs(replay_dir, exist_ok=True)
    os.makedirs(code_dir, exist_ok=True)
    os.makedirs(ro_dir, exist_ok=True)
    
    return code_dir, replay_dir, ro_dir