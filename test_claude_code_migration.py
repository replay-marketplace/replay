#!/usr/bin/env python3
"""
Test script to demonstrate the Claude Code migration.

This script shows how the new configuration loading works and provides
examples of how to set up Claude Code with your system.
"""

import os
import sys
import logging
from pathlib import Path

# Add the core directory to the Python path
sys.path.insert(0, 'core')

from core.backend.claude_code_config import ClaudeCodeConfig
from core.backend.replay import Replay, InputConfig

def setup_logging():
    """Set up logging to see the configuration details."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def test_claude_code_config():
    """Test the Claude Code configuration loading."""
    print("=== Testing Claude Code Configuration ===")
    
    config = ClaudeCodeConfig()
    config.log_configuration_status()
    
    print(f"Claude Code configured: {config.is_claude_code_configured()}")
    print(f"Client kwargs: {config.get_client_kwargs()}")
    
    return config

def demo_environment_setup():
    """Demonstrate how to set up Claude Code environment variables."""
    print("\n=== Claude Code Environment Setup ===")
    print("To use Claude Code, set these environment variables:")
    print("export ANTHROPIC_AUTH_TOKEN='your-auth-token-here'")
    print("export ANTHROPIC_BASE_URL='your-claude-code-base-url-here'")
    print()
    print("Alternatively, create ~/.claude/settings.json with:")
    print("""{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-auth-token-here"
  }
}""")
    print()
    print("Current environment status:")
    print(f"ANTHROPIC_AUTH_TOKEN: {'SET' if os.environ.get('ANTHROPIC_AUTH_TOKEN') else 'NOT SET'}")
    print(f"ANTHROPIC_BASE_URL: {'SET' if os.environ.get('ANTHROPIC_BASE_URL') else 'NOT SET'}")
    print(f"ANTHROPIC_API_KEY: {'SET' if os.environ.get('ANTHROPIC_API_KEY') else 'NOT SET'}")

def test_replay_initialization():
    """Test that Replay can initialize with the new configuration."""
    print("\n=== Testing Replay Initialization ===")
    
    try:
        # Create a minimal config for testing
        input_config = InputConfig(
            input_prompt_file="test_prompt.txt",
            project_name="test_project",
            output_dir="test_output"
        )
        
        # Try to create a Replay instance with mock client
        replay = Replay.from_recipe(input_config, use_mock=True)
        print("✓ Replay initialization successful with mock client")
        
        # Check if the client was properly initialized
        if hasattr(replay, 'client') and replay.client is not None:
            print("✓ Client wrapper created successfully")
        else:
            print("✗ Client wrapper not created")
            
    except Exception as e:
        print(f"✗ Replay initialization failed: {e}")

def main():
    """Main test function."""
    setup_logging()
    
    print("Claude Code Migration Test")
    print("=" * 50)
    
    # Test configuration loading
    config = test_claude_code_config()
    
    # Show environment setup
    demo_environment_setup()
    
    # Test Replay initialization
    # test_replay_initialization()
    
    print("\n" + "=" * 50)
    print("Migration Test Complete")
    
    if config.is_claude_code_configured():
        print("✓ Claude Code is properly configured and ready to use!")
    else:
        print("ℹ Claude Code is not configured. Set ANTHROPIC_AUTH_TOKEN and ANTHROPIC_BASE_URL to use Claude Code.")
        if os.environ.get('ANTHROPIC_API_KEY'):
            print("✓ Fallback to standard Anthropic API is available.")
        else:
            print("⚠ No authentication method available. Please configure Claude Code or set ANTHROPIC_API_KEY.")

if __name__ == "__main__":
    main() 
