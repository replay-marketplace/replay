from typing import Tuple
from .dir_preprocessing import setup_project_directories as _setup_project_directories

def setup_project_directories(output_dir: str, project_name: str) -> Tuple[str, str]:
    """
    Set up project directories for replay and code storage.
    
    Args:
        output_dir (str): Base output directory path
        project_name (str): Name of the project
        
    Returns:
        Tuple[str, str]: Paths to replay and code directories
        
    Raises:
        FileNotFoundError: If output_dir doesn't exist
    """
    return _setup_project_directories(output_dir, project_name)

__all__ = ['setup_project_directories'] 