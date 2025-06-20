import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.append(project_root)

from core.dir_preprocessing import setup_project_directories

def main():
    # Create a test directory in the current working directory
    output_dir = os.path.join(os.getcwd(), "test_output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up directories for a test project
    project_name = "example_project"
    print(f"Setting up directories in: {output_dir}")
    print(f"Project name: {project_name}")
    
    # Create the directory structure
    replay_dir, code_dir = setup_project_directories(output_dir, project_name)
    
    print("\nCreated directories:")
    print(f"Replay directory: {replay_dir}")
    print(f"Code directory: {code_dir}")
    
    # Create the structure again to demonstrate counter increment
    print("\nCreating another set of directories...")
    replay_dir2, code_dir2 = setup_project_directories(output_dir, project_name)
    
    print("\nCreated new directories:")
    print(f"Replay directory: {replay_dir2}")
    print(f"Code directory: {code_dir2}")

if __name__ == "__main__":
    main() 