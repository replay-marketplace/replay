#!/usr/bin/env python3
"""
Step-by-step execution example for the replay package.

This example demonstrates how to execute the replay system step by step,
allowing for inspection and debugging at each stage.
"""

import os
import tempfile
import json
from core import Replay, InputConfig, ReplayState


def create_multi_step_prompt():
    """Create a prompt with multiple steps for demonstration."""
    prompt_content = """
    Create a simple calculator with multiple operations.
    
    /TEMPLATE
    def add(a, b):
        return a + b
    
    def subtract(a, b):
        return a - b
    
    def multiply(a, b):
        return a * b
    
    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    /RUN
    python -c "
    from calculator import add, subtract, multiply, divide
    print('Testing calculator functions...')
    print(f'2 + 3 = {add(2, 3)}')
    print(f'5 - 2 = {subtract(5, 2)}')
    print(f'4 * 6 = {multiply(4, 6)}')
    print(f'10 / 2 = {divide(10, 2)}')
    "
    
    /CONDITIONAL
    Check if all basic operations work correctly
    
    /TEMPLATE
    def test_calculator():
        assert add(2, 3) == 5
        assert subtract(5, 2) == 3
        assert multiply(4, 6) == 24
        assert divide(10, 2) == 5
        print('All tests passed!')
    
    /RUN
    python -c "from calculator import test_calculator; test_calculator()"
    """
    return prompt_content


def main():
    """Main example function demonstrating step-by-step execution."""
    print("Replay Package - Step-by-Step Execution Example")
    print("=" * 60)
    
    # Create a temporary directory for this example
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Working in temporary directory: {temp_dir}")
        
        # Create a sample prompt file
        prompt_file = os.path.join(temp_dir, "calculator_prompt.txt")
        with open(prompt_file, "w") as f:
            f.write(create_multi_step_prompt())
        
        print(f"Created sample prompt file: {prompt_file}")
        
        # Set up the input configuration
        config = InputConfig(
            input_prompt_file=prompt_file,
            project_name="calculator_example",
            output_dir=os.path.join(temp_dir, "output")
        )
        
        # Create the replay instance
        print("\nCreating Replay instance...")
        replay = Replay(input_config=config)
        
        print("Replay instance created successfully!")
        
        # Step 1: Setup
        print("\n" + "="*50)
        print("STEP 1: Setup")
        print("="*50)
        
        # Note: In a real scenario, you would need to set ANTHROPIC_API_KEY
        # For this example, we'll just demonstrate the setup process
        print("Setting up directories and loading system instructions...")
        
        # Create mock system instructions
        instructions_dir = os.path.join(temp_dir, "input_const")
        os.makedirs(instructions_dir, exist_ok=True)
        with open(os.path.join(instructions_dir, "client_instructions_with_json.txt"), "w") as f:
            f.write("You are a helpful AI assistant that generates code.")
        
        # Change to temp directory for setup
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            # Mock the setup (in real scenario, this would initialize the client)
            print("✓ Directories created")
            print("✓ System instructions loaded")
            print("✓ Client initialized (mocked)")
            
            replay.state.init.setup_done = True
            print("✓ Setup completed")
            
        finally:
            os.chdir(original_cwd)
        
        # Step 2: Preprocessing
        print("\n" + "="*50)
        print("STEP 2: Preprocessing")
        print("="*50)
        
        print("Processing prompt and building execution graph...")
        
        # In a real scenario, this would call prompt_preprocess3
        # For this example, we'll create a mock graph
        from core.prompt_preprocess2.ir.ir import EpicIR, Opcode
        
        epic = EpicIR()
        node1 = epic.add_node(Opcode.PROMPT, {"prompt": "Create calculator"})
        node2 = epic.add_node(Opcode.TEMPLATE, {"template": "def add(a, b): return a + b"})
        node3 = epic.add_node(Opcode.RUN, {"command": "python test.py"})
        node4 = epic.add_node(Opcode.CONDITIONAL, {"condition": "Check if tests pass"})
        node5 = epic.add_node(Opcode.EXIT, {})
        
        epic.graph.add_edge(node1, node2)
        epic.graph.add_edge(node2, node3)
        epic.graph.add_edge(node3, node4)
        epic.graph.add_edge(node4, node5)
        epic.first_node = node1
        
        replay.epic = epic
        replay.dfs_nodes = list(replay.epic.graph.nodes())
        replay.state.init.preprocess_done = True
        
        print(f"✓ Graph built with {len(replay.dfs_nodes)} nodes")
        print("✓ Preprocessing completed")
        
        # Step 3: Step-by-step execution
        print("\n" + "="*50)
        print("STEP 3: Step-by-Step Execution")
        print("="*50)
        
        step_count = 0
        while replay.has_steps():
            step_count += 1
            current_node = replay.dfs_nodes[replay.state.execution.current_node_idx]
            opcode = replay.epic.graph.nodes[current_node]['opcode']
            
            print(f"\nStep {step_count}: Processing {opcode.name} node '{current_node}'")
            print(f"  Node contents: {replay.epic.graph.nodes[current_node]['contents']}")
            
            # In a real scenario, this would call the appropriate processor
            print(f"  ✓ {opcode.name} processing completed")
            
            replay.state.execution.current_node_idx += 1
            
            # Save state after each step
            replay.save_state()
            print(f"  ✓ State saved")
        
        print(f"\n✓ All {step_count} steps completed!")
        replay.state.execution.finished = True
        
        # Final state
        print("\n" + "="*50)
        print("FINAL STATE")
        print("="*50)
        print(f"  - Setup done: {replay.state.init.setup_done}")
        print(f"  - Preprocess done: {replay.state.init.preprocess_done}")
        print(f"  - Execution finished: {replay.state.execution.finished}")
        print(f"  - Steps completed: {step_count}")
        
        print("\nExample completed successfully!")
        print("\nTo run this with actual API calls, set the ANTHROPIC_API_KEY environment variable:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")


if __name__ == "__main__":
    main() 