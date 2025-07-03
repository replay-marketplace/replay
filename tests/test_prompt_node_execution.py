from pathlib import Path
from core.backend.replay import Replay, InputConfig
from core.backend.client.mock_anthropic import MockAnthropicClient

def test_prompt_node_execution_step_by_step(tmp_path):
    """Test prompt node execution step by step with direct access to mock client data."""
    prompt_file = Path("tests/cli_project/prompt.txt")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    project_name = "test_prompt_execution"

    # Create input config
    input_config = InputConfig(
        input_prompt_file=str(prompt_file),
        project_name=project_name,
        output_dir=str(output_dir)
    )

    # Create replay instance with mock client
    replay = Replay.from_recipe(input_config, use_mock=True)
    
    # Get the mock client instance through the wrapper
    mock_client = replay.client.client  # Access the underlying mock client
    assert isinstance(mock_client, MockAnthropicClient), "Client should be MockAnthropicClient"
    
    # Clear any previous captured data
    mock_client.captured_jsons = []
    
    # Debug: Check initial state
    print(f"Initial status: {replay.state.status}")
    print(f"Has steps: {replay.has_steps()}")
    print(f"Current node idx: {replay.state.execution.current_node_idx}")
    print(f"DFS nodes: {replay.state.execution.dfs_nodes}")
    
    # Compile the replay to set up the execution graph
    replay.compile()
    
    # Debug: Check state after compilation
    print(f"After compilation status: {replay.state.status}")
    print(f"Has steps: {replay.has_steps()}")
    print(f"Current node idx: {replay.state.execution.current_node_idx}")
    print(f"DFS nodes: {replay.state.execution.dfs_nodes}")
    
    # Track file modifications across steps
    file_modifications = {}
    
    # Run step by step and inspect each step
    step_count = 0
    max_steps = 20  # Safety limit
    
    while replay.has_steps() and step_count < max_steps:
        print(f"\n=== Step {step_count + 1} ===")
        
        # Get current node info before processing
        if replay.state.execution.current_node_idx < len(replay.state.execution.dfs_nodes):
            current_node = replay.state.execution.dfs_nodes[replay.state.execution.current_node_idx]
            node_data = replay.state.execution.epic.graph.nodes[current_node]
            opcode = node_data['opcode']
            contents = node_data.get('contents', {})
            
            print(f"Processing node: {current_node}")
            print(f"Opcode: {opcode}")
            print(f"Contents: {contents}")
        
        # Capture the number of requests before this step
        requests_before = len(mock_client.captured_jsons)
        
        # Run the step
        replay.run_step()
        
        # Check if any new requests were made
        requests_after = len(mock_client.captured_jsons)
        new_requests = requests_after - requests_before
        
        if new_requests > 0:
            print(f"New requests made in this step: {new_requests}")
            
            # Inspect the new requests
            for i in range(requests_before, requests_after):
                request = mock_client.captured_jsons[i]
                print(f"\n--- Request {i + 1} ---")
                print(f"Prompt: {request.get('prompt', 'No prompt')}")
                
                # Check code_to_edit
                code_to_edit = request.get('code_to_edit', [])
                if code_to_edit:
                    print(f"Code to edit files: {[f['path_and_filename'] for f in code_to_edit]}")
                    for file_info in code_to_edit:
                        print(f"  {file_info['path_and_filename']}: {len(file_info['contents'])} chars")
                        # Track file modifications
                        file_modifications[file_info['path_and_filename']] = file_info['contents']
                
                # Check read_only_files
                read_only_files = request.get('read_only_files', [])
                if read_only_files:
                    print(f"Read-only files: {[f['path_and_filename'] for f in read_only_files]}")
                    for file_info in read_only_files:
                        print(f"  {file_info['path_and_filename']}: {len(file_info['contents'])} chars")
        
        step_count += 1
    
    # Verify we captured the expected requests (now 4 prompts)
    assert len(mock_client.captured_jsons) >= 4, f"Expected at least 4 prompt requests, got {len(mock_client.captured_jsons)}"
    
    # Test specific prompt requests
    prompt_requests = [req for req in mock_client.captured_jsons if req.get('prompt')]
    
    # First prompt: "Hello! We are referencing @docs:doc1.md"
    first_prompt = next((req for req in prompt_requests if "Hello! We are referencing @docs:doc1.md" in req.get('prompt', '')), None)
    assert first_prompt is not None, "First prompt request not found"
    
    # Check that read_only_files contains the docs reference
    read_only_files = first_prompt.get('read_only_files', [])
    doc_files = [f['path_and_filename'] for f in read_only_files]
    assert "doc1.md" in doc_files, f"Expected doc1.md in read_only_files, got {doc_files}"
    
    # Verify the content of the doc file
    doc_file = next((f for f in read_only_files if f['path_and_filename'] == 'doc1.md'), None)
    assert doc_file is not None, "doc1.md file not found in read_only_files"
    assert doc_file['contents'] == "This is an document", f"Expected doc content, got {doc_file['contents']}"
    
    # Second prompt: "Wow! Can I also reference from @template:template1.py"
    second_prompt = next((req for req in prompt_requests if "Wow! Can I also reference from @template:template1.py" in req.get('prompt', '')), None)
    assert second_prompt is not None, "Second prompt request not found"
    
    # Check that read_only_files contains the template reference
    read_only_files = second_prompt.get('read_only_files', [])
    template_files = [f['path_and_filename'] for f in read_only_files]
    assert "template1.py" in template_files, f"Expected template1.py in read_only_files, got {template_files}"
    
    # Verify the content of the template file
    template_file = next((f for f in read_only_files if f['path_and_filename'] == 'template1.py'), None)
    assert template_file is not None, "template1.py file not found in read_only_files"
    assert template_file['contents'] == "# This is a template file", f"Expected template content, got {template_file['contents']}"
    
    # Third prompt: "No way! Even @code:template1.py"
    third_prompt = next((req for req in prompt_requests if "No way! Even @code:template1.py" in req.get('prompt', '')), None)
    assert third_prompt is not None, "Third prompt request not found"
    
    # Check that code_to_edit contains the code reference
    code_to_edit = third_prompt.get('code_to_edit', [])
    code_files = [f['path_and_filename'] for f in code_to_edit]
    # The code_to_edit should contain the full path, so we check if it ends with template1.py
    assert any(f.endswith('template1.py') for f in code_files), f"Expected template1.py in code_to_edit, got {code_files}"
    
    # Verify the content of the code file (should be original content)
    code_file = next((f for f in code_to_edit if f['path_and_filename'].endswith('template1.py')), None)
    assert code_file is not None, "template1.py file not found in code_to_edit"
    assert code_file['contents'] == "# This is a template file", f"Expected code content, got {code_file['contents']}"
    
    # Fourth prompt: "More edits to @code:template1.py"
    fourth_prompt = next((req for req in prompt_requests if "More edits to @code:template1.py" in req.get('prompt', '')), None)
    assert fourth_prompt is not None, "Fourth prompt request not found"
    
    # Check that code_to_edit contains the code reference again
    code_to_edit = fourth_prompt.get('code_to_edit', [])
    code_files = [f['path_and_filename'] for f in code_to_edit]
    assert any(f.endswith('template1.py') for f in code_files), f"Expected template1.py in code_to_edit, got {code_files}"
    
    # CRITICAL: Verify that the fourth prompt sees the MODIFIED content from the third prompt
    code_file = next((f for f in code_to_edit if f['path_and_filename'].endswith('template1.py')), None)
    assert code_file is not None, "template1.py file not found in code_to_edit for fourth prompt"
    
    # The content should now be the modified version from the third prompt
    expected_modified_content = "# Modified by LLM: # This is a template file"
    assert code_file['contents'] == expected_modified_content, f"Fourth prompt should see modified content, got: {code_file['contents']}"
    
    # Verify that files were actually written to disk with updated content
    print(f"\n=== Verifying file modifications on disk ===")
    
    # Check the code directory for written files
    code_dir = Path(replay.code_dir)
    assert code_dir.exists(), f"Code directory should exist: {code_dir}"
    
    # Look for the template1.py file that should have been modified
    template_file_path = None
    for file_path in code_dir.rglob("template1.py"):
        template_file_path = file_path
        break
    
    assert template_file_path is not None, f"template1.py should exist in code directory: {code_dir}"
    assert template_file_path.exists(), f"template1.py file should exist: {template_file_path}"
    
    # Read the actual file content from disk
    actual_content = template_file_path.read_text()
    print(f"Actual file content on disk: {repr(actual_content)}")
    
    # Verify that the file contains the LLM modification
    assert "# Modified by LLM:" in actual_content, f"File should contain LLM modification marker, got: {actual_content}"
    assert "# This is a template file" in actual_content, f"File should contain original content, got: {actual_content}"
    
    # The file should have been modified twice (third and fourth prompts)
    # Each modification adds another "# Modified by LLM:" prefix
    expected_final_content = "# Modified by LLM: # Modified by LLM: # This is a template file"
    assert actual_content == expected_final_content, f"File content should match expected double modification, got: {actual_content}"