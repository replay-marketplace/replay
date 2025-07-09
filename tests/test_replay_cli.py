import subprocess
import os
import sys
import shutil
import tempfile
import pytest
import json
from pathlib import Path
from core.backend.client.mock_anthropic import MockAnthropicClient

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s')

def assert_files_exact(output_dir, expected_files):
    # Collect all files in output_dir (relative paths), excluding client/ and .git/ directories
    actual_files = set()
    for root, dirs, files in os.walk(output_dir):
        # Skip client directories that contain timestamp-dependent files
        if "client" in Path(root).parts:
            continue
        # Skip .git directories that contain git repository files
        if ".git" in Path(root).parts:
            continue
        for file in files:
            abs_path = Path(root) / file
            rel_path = abs_path.relative_to(output_dir)
            actual_files.add(str(rel_path))
    expected_set = set(expected_files)
    assert actual_files == expected_set, f"Files mismatch.\nExpected: {expected_set}\nActual: {actual_files}"

def print_tree(path, indent=0):
    # print nicely formatted/indented output_dir treeview (deep) recursively
    for root, dirs, files in os.walk(path):
        level = root.replace(str(path), '').count(os.sep)
        indent = level
        print("  " * indent + os.path.basename(root))
        for file in files:
            print("  " * (indent + 1) + file)

def check_git_repo(version_dir):
    """Check that git repository exists and is valid."""
    git_dir = version_dir / ".git"
    if not git_dir.exists():
        return False, f"Git repository not found in {version_dir}"
    
    try:
        # Check if it's a valid git repository
        result = subprocess.run(["git", "status"], cwd=version_dir, 
                              capture_output=True, text=True, check=True)
        return True, "Git repository is valid"
    except subprocess.CalledProcessError as e:
        return False, f"Git repository is invalid: {e}"

def test_replay_cli_run_all(tmp_path):
    prompt_file = Path("tests/cli_project/prompt.txt")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    project_name = "test_project"

    with open("tests/cli_project/expected_files_all.json") as f:
        expected = json.load(f)
    expected_files = expected["files"]

    result = subprocess.run([
        sys.executable, "replay.py",
        str(prompt_file), project_name, "--output_dir", str(output_dir), "--mock"
    ], capture_output=True, text=True, env=os.environ.copy())
    assert result.returncode == 0, f"run_all failed: {result.stderr}"
    print_tree(output_dir)
    assert_files_exact(output_dir, expected_files)
    
    # Check that git repository was created
    version_dir = output_dir / project_name / "1"
    is_valid, message = check_git_repo(version_dir)
    assert is_valid, message
    print(f"✓ {message}")
    
    # Check that there are commits (at least initial commit)
    result = subprocess.run(["git", "rev-list", "--count", "HEAD"], 
                          cwd=version_dir, capture_output=True, text=True, check=True)
    commit_count = int(result.stdout.strip())
    assert commit_count > 0, f"Expected at least 1 commit, got {commit_count}"
    print(f"✓ Git repository has {commit_count} commits")

def test_replay_cli_step_by_step(tmp_path):        
    prompt_file = Path("tests/cli_project/prompt.txt")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    project_name = "test_project_step_by_step"

    with open("tests/cli_project/expected_files_step_by_step.json") as f:
        expected = json.load(f)
    steps = expected["steps"]

    # Run once to create the session folder
    print(f"Running step 0")
    result = subprocess.run([
        sys.executable, "replay.py",
        str(prompt_file), project_name, "--output_dir", str(output_dir), "--mock", "--setup_only"
    ], capture_output=True, text=True, env=os.environ.copy())    
    assert result.returncode == 0, f"initial run failed: {result.stderr}"
    
    print_tree(output_dir)
    
    # Check that git repository was created after initial setup
    version_dir = output_dir / project_name / "1"
    is_valid, message = check_git_repo(version_dir)
    assert is_valid, message
    print(f"✓ {message}")
    
    # Get initial commit count
    result = subprocess.run(["git", "rev-list", "--count", "HEAD"], 
                          cwd=version_dir, capture_output=True, text=True, check=True)
    initial_commit_count = int(result.stdout.strip())
    print(f"Initial commit count: {initial_commit_count}")
    
    # Verify initial commit message
    result = subprocess.run(["git", "log", "-1", "--pretty=format:%s"], 
                          cwd=version_dir, capture_output=True, text=True, check=True)
    initial_commit_message = result.stdout.strip()
    print(f"Initial commit message: {initial_commit_message}")
    assert initial_commit_message == "Initial project setup", \
        f"Initial commit message should be 'Initial project setup', got: {initial_commit_message}"
    
    # Now run step mode until done, checking files and git commits after each step
    max_steps = 30
    previous_commit_count = initial_commit_count
    
    for step_idx in range(1, max_steps):
        print(f"Running step {step_idx}")
        result = subprocess.run([
            sys.executable, "replay.py",
            project_name, "--output_dir", str(output_dir), "--step", "--mock"
        ], capture_output=True, text=True, env=os.environ.copy())
        if result.returncode == 42:
            print("No more steps to run.")
            break
        assert result.returncode == 0, f"step mode failed: {result.stderr}"
        
        # Check that git repository still exists and is valid
        is_valid, message = check_git_repo(version_dir)
        assert is_valid, f"Git repository issue after step {step_idx}: {message}"
        
        # Check commit count increased
        result = subprocess.run(["git", "rev-list", "--count", "HEAD"], 
                              cwd=version_dir, capture_output=True, text=True, check=True)
        current_commit_count = int(result.stdout.strip())
        print(f"Step {step_idx} commit count: {current_commit_count}")
        
        # Commit count should increase (unless no changes were made)
        if current_commit_count < previous_commit_count:
            raise AssertionError(f"Commit count decreased from {previous_commit_count} to {current_commit_count} at step {step_idx}")
        
        # Get latest commit message
        result = subprocess.run(["git", "log", "-1", "--pretty=format:%s"], 
                              cwd=version_dir, capture_output=True, text=True, check=True)
        latest_commit_message = result.stdout.strip()
        print(f"Step {step_idx} commit message: {latest_commit_message}")
        
        # Verify commit message format
        assert latest_commit_message.startswith(f"Step {step_idx}:"), \
            f"Commit message doesn't match expected format: {latest_commit_message}"
        
        previous_commit_count = current_commit_count
        
        if step_idx < len(steps):
            assert_files_exact(output_dir, steps[step_idx]["files"])        
    else:
        raise AssertionError(f"Step-by-step test exceeded {max_steps} steps without finishing.")
    
    print(f"✓ Git repository maintained throughout execution with {previous_commit_count} total commits") 