import os
import pytest
from pathlib import Path
from core.dir_preprocessing import setup_project_directories

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary directory for testing."""
    return str(tmp_path)

def test_setup_project_directories_creates_initial_structure(temp_output_dir):
    """Test that the function creates the initial directory structure correctly."""
    project_name = "test_project"
    replay_dir, code_dir = setup_project_directories(temp_output_dir, project_name)
    
    # Check that the project directory exists
    project_dir = os.path.join(temp_output_dir, project_name)
    assert os.path.exists(project_dir)
    
    # Check that replay_counter.txt exists and contains "0"
    counter_file = os.path.join(project_dir, "replay_counter.txt")
    assert os.path.exists(counter_file)
    with open(counter_file, "r") as f:
        assert f.read().strip() == "1"  # Should be 1 after first run
    
    # Check that the numbered directory exists
    numbered_dir = os.path.join(project_dir, "1")
    assert os.path.exists(numbered_dir)
    
    # Check that replay and code directories exist
    assert os.path.exists(replay_dir)
    assert os.path.exists(code_dir)
    
    # Check that returned paths are correct
    assert replay_dir == os.path.join(numbered_dir, "replay")
    assert code_dir == os.path.join(numbered_dir, "code")

def test_setup_project_directories_increments_counter(temp_output_dir):
    """Test that the function increments the counter correctly."""
    project_name = "test_project"
    
    # First run
    setup_project_directories(temp_output_dir, project_name)
    
    # Second run
    replay_dir, code_dir = setup_project_directories(temp_output_dir, project_name)
    
    # Check counter value
    counter_file = os.path.join(temp_output_dir, project_name, "replay_counter.txt")
    with open(counter_file, "r") as f:
        assert f.read().strip() == "2"
    
    # Check that new numbered directory exists
    numbered_dir = os.path.join(temp_output_dir, project_name, "2")
    assert os.path.exists(numbered_dir)

def test_setup_project_directories_nonexistent_output_dir():
    """Test that the function raises FileNotFoundError for nonexistent output directory."""
    with pytest.raises(FileNotFoundError):
        setup_project_directories("/nonexistent/path", "test_project") 