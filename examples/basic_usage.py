#!/usr/bin/env python3
"""
Basic usage example for the replay package.

This example demonstrates how to use the replay package programmatically
to process a prompt and generate code.
"""

import os
import tempfile
from core import Replay, InputConfig


def create_sample_prompt():
    """Create a sample prompt file for testing."""
    prompt_content = """
    Create a simple Python function to calculate the factorial of a number.
    
    /TEMPLATE
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)
    
    /RUN
    python -c "from factorial import factorial; print(factorial(5))"
    
    /CONDITIONAL
    Check if the function works correctly
    """
    return prompt_content


def main():
    """Main example function."""
    print("Replay Package - Basic Usage Example")
    print("=" * 50)
    
    # Create a temporary directory for this example
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Working in temporary directory: {temp_dir}")
        
        # Create a sample prompt file
        prompt_file = os.path.join(temp_dir, "sample_prompt.txt")
        with open(prompt_file, "w") as f:
            f.write(create_sample_prompt())
        
        print(f"Created sample prompt file: {prompt_file}")
        
        # Set up the input configuration
        config = InputConfig(
            input_prompt_file=prompt_file,
            project_name="factorial_example",
            output_dir=os.path.join(temp_dir, "output")
        )
        
        print("Input configuration created:")
        print(f"  - Input file: {config.input_prompt_file}")
        print(f"  - Project name: {config.project_name}")
        print(f"  - Output directory: {config.output_dir}")
        
        # Create the replay instance
        print("\nCreating Replay instance...")
        replay = Replay(input_config=config)
        
        # Note: In a real scenario, you would need to set ANTHROPIC_API_KEY
        # For this example, we'll just demonstrate the setup
        print("Replay instance created successfully!")
        
        # Show the state
        print(f"\nInitial state:")
        print(f"  - Setup done: {replay.state.init.setup_done}")
        print(f"  - Preprocess done: {replay.state.init.preprocess_done}")
        print(f"  - Execution finished: {replay.state.execution.finished}")
        
        print("\nExample completed successfully!")
        print("\nTo run this with actual API calls, set the ANTHROPIC_API_KEY environment variable:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")


if __name__ == "__main__":
    main() 