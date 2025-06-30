import subprocess
import os
import sys
import shutil
import tempfile
import pytest
import json
from pathlib import Path
from core.backend.mock_anthropic import MockAnthropicClient

def assert_files_exact(output_dir, expected_files):
    # Collect all files in output_dir (relative paths), excluding client/ directory
    actual_files = set()
    for root, dirs, files in os.walk(output_dir):
        # Skip client directories that contain timestamp-dependent files
        if "client" in Path(root).parts:
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
    
    # Now run step mode until done, checking files after each step
    max_steps = 30    
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
        if step_idx < len(steps):
            assert_files_exact(output_dir, steps[step_idx]["files"])        
    else:
        raise AssertionError(f"Step-by-step test exceeded {max_steps} steps without finishing.") 