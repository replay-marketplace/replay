### Tool Installation Guide

This guide assumes you have already installed and set up Claude Code and related dependencies. Do those steps before installing tools.

#### 1. Install

Run this code from the root directory of replay to install the tools and make them discoverable to Claude Code:

```bash
git submodule update --init tools/api_database_tools # Initialize the tools submodule
cd tools/api_database_tools
pip install . # Install the MCP package
claude mcp add -- tt-metal-tools python server.py # Register the MCP with Claude Code
cd ../..
```

**Important Note**: The MCP server registration creates a project-specific configuration tied to the `tools/api_database_tools` directory. However, the tools are designed to work automatically when called via the Claude Code SDK (which is how `replay.py` uses them). The directory-specific registration is intentional and ensures proper tool functionality during programmatic usage.

#### 2. Verify

You can verify the tools are installed correctly by running the following command from the `tools/api_database_tools` directory:

```bash
cd tools/api_database_tools
claude mcp list
```

This is the expected output:

```
Checking MCP server health...

tt-metal-tools: python server.py - ✓ Connected
```

If you want to see the tools working, or the format of output it feeds to the model, you can run the following command:

```bash
pytest -s tests/test_all_tools.py
```

#### Troubleshooting

**Directory-Specific MCP Configuration**: The MCP server registration is tied to the specific directory where it was registered (`tools/api_database_tools`). This means:
- `claude mcp list` will show "✗ Failed to connect" when run from the repo root directory
- `claude mcp list` will show "✓ Connected" when run from the `tools/api_database_tools` directory
- This behavior is intentional and does not affect SDK usage (which is how `replay.py` accesses the tools)

**Common Issues**:
- If `claude mcp list` shows no tools at all, the `pip install .` or `claude mcp add` command didn't work correctly
- If you can see the tools but they can't connect from the `tools/api_database_tools` directory, try:
  1. `claude mcp remove tt-metal-tools`
  2. Make sure you are in the `tools/api_database_tools` directory
  3. Run: `claude mcp add -- tt-metal-tools python server.py`

**Testing Tools**: The tools will work automatically when `replay.py` calls them via the Claude Code SDK, regardless of which directory you run `replay.py` from.
