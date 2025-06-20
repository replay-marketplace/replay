# Directory Preprocessing

A simple utility to set up project directories for replay and code storage.

## Usage

```python
from core.dir_preprocessing import setup_project_directories

# Set up directories for your project
replay_dir, code_dir = setup_project_directories(
    output_dir="/path/to/output",
    project_name="my_project"
)

# replay_dir and code_dir will contain paths to the created directories
print(f"Replay directory: {replay_dir}")
print(f"Code directory: {code_dir}")
```

The function will:
1. Create a project directory if it doesn't exist
2. Manage a replay counter
3. Create numbered replay directories
4. Set up replay and code subdirectories
5. Return paths to the created directories 