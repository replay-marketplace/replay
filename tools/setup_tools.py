#!/usr/bin/env python3
"""One-time setup for the replay system with API tools."""

import os
import sys
from pathlib import Path

def setup_api_tools():
    """Set up API database tools for the replay system."""
    print("Setting up API database tools for replay system...")
    
    # Just check that the api_database_tools module is accessible
    try:
        import api_database_tools
        print("✓ API database tools module found")
    except ImportError:
        print("✗ API database tools module not found")
        print("Please ensure api_database_tools is in your Python path")
        return False
    
    # Check for TT_METAL_HOME
    if not os.environ.get("TT_METAL_HOME"):
        print("\nIMPORTANT: TT_METAL_HOME environment variable not set!")
        print("Please set it to your tt-metal repository path:")
        print("  export TT_METAL_HOME=/path/to/tt-metal")
        print("\nOnce set, the API databases will be built automatically on first use.")
        return False
    
    print("\nSetup complete! The API tools will be available automatically when you run replay.")
    return True

if __name__ == "__main__":
    success = setup_api_tools()
    sys.exit(0 if success else 1)