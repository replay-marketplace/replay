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
    # Collect all files in output_dir (relative paths)
    actual_files = set()
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            abs_path = Path(root) / file
            rel_path = abs_path.relative_to(output_dir)
            actual_files.add(str(rel_path))
    expected_set = set(expected_files)
    assert actual_files == expected_set, f"Files mismatch.\nExpected: {expected_set}\nActual: {actual_files}"

def print_tree(path, indent=0):
    # print nicely formatted/indented output_dir treeview (deep) recursively
    for root, dirs, files in os.walk(path):
        print("  " * indent + os.path.basename(root))
        for file in files:
            print("  " * (indent + 1) + file)
        for d in dirs:
            print_tree(Path(root) / d, indent + 1)

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
        str(prompt_file), project_name, "--output_dir", str(output_dir)
    ], capture_output=True, text=True, env=os.environ.copy())
    assert result.returncode == 0, f"run_all failed: {result.stderr}"
    print_tree(output_dir)
    assert_files_exact(output_dir, expected_files)

def test_replay_cli_step_by_step(tmp_path):        
    prompt_file = Path("tests/cli_project/prompt.txt")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    project_name = "test_project"

    with open("tests/cli_project/expected_files_step_by_step.json") as f:
        expected = json.load(f)
    steps = expected["steps"]

    # Run once to create the session folder
    result = subprocess.run([
        sys.executable, "replay.py",
        str(prompt_file), project_name, "--output_dir", str(output_dir)
    ], capture_output=True, text=True, env=os.environ.copy())    
    assert result.returncode == 0, f"initial run failed: {result.stderr}"
    
    print_tree(output_dir)

    session_folder = None
    for root, dirs, files in os.walk(output_dir):
        for d in dirs:
            if (Path(root) / d / "replay_state.json").exists():
                session_folder = str(Path(root) / d)
                break
    assert session_folder, "Session folder with replay_state.json not found"
    
    # Now run step mode until done, checking files after each step
    max_steps = 10
    step_idx = 0
    for _ in range(max_steps):
        result = subprocess.run([
            sys.executable, "replay.py",
            "--session_folder", session_folder, "--step"
        ], capture_output=True, text=True, env=os.environ.copy())
        assert result.returncode == 0, f"step mode failed: {result.stderr}"
        if step_idx < len(steps):
            assert_files_exact(output_dir, steps[step_idx]["files"])
        else:
            raise AssertionError(f"More steps executed than expected ({len(steps)})")
        step_idx += 1
        if "No more steps to run." in result.stdout:
            break
    else:
        raise AssertionError(f"Step-by-step test exceeded {max_steps} steps without finishing.") 