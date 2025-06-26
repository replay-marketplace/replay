import os
import shutil
from pathlib import Path
from typing import Tuple    

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
            1 /
            2 /
            3 /                     <--- epic_dir
                code/
                read_only/
                replay/
            latest/                 <--- latest generted replay directory
                code/
                read_only/
                replay/
            .replay.txt
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

        # Create latest/ dir  
        replay_master_dir = os.path.join(project_dir, "replay")
        os.makedirs(replay_master_dir, exist_ok=False)
        
        # Create .replay/ dir  
        latest_dir = os.path.join(project_dir, "latest")
        os.makedirs(latest_dir, exist_ok=False)

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
    ro_dir = os.path.join(epic_dir, "read_only")
    os.makedirs(replay_dir, exist_ok=True)
    os.makedirs(code_dir, exist_ok=True)
    os.makedirs(ro_dir, exist_ok=True)
    
    return code_dir, replay_dir, ro_dir, project_dir, latest_dir, epic_dir
    

def post_replay_dir_cleanup(project_dir: str, latest_dir: str, epic_dir: str):
    """
    This function is called after the replay directory is created.
    It will copy the latest epic in to latest/ directory. 
    """
    print("\n\nDir post processing:")

    # Delete all files and subdirectories in latest/
    for item in os.listdir(latest_dir):
        item_path = os.path.join(latest_dir, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
        print(f"removed {item} from latest/")

    # Copy all files and subdirectories from epic_dir into latest/
    print(os.listdir(epic_dir))
    for item in os.listdir(epic_dir):
        src_path = os.path.join(epic_dir, item)
        dst_path = os.path.join(latest_dir, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
        print(f"copied {item} to latest/")
    
    