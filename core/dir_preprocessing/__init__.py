from typing import Tuple
from .dir_preprocessing import setup_project_directories as _setup_project_directories
from .dir_preprocessing import post_replay_dir_cleanup as _post_replay_dir_cleanup

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

def post_replay_dir_cleanup(project_dir: str, latest_dir: str, epic_dir: str):
    """
    This function is called after the replay directory is created.
    It will copy the latest epic in to latest/ directory. 
    """
    return _post_replay_dir_cleanup(project_dir, latest_dir, epic_dir)
__all__ = ['setup_project_directories', 'post_replay_dir_cleanup'] 