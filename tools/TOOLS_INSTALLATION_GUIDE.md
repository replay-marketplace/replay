### Tool Installation Guide

This guide assumes you have already installed and set up Claude Code and related dependencies. Do those steps before installing tools.

#### 1. Install

Run this code from the root directory of replay to install the tools and make them discoverable to Claude Code:

```bash
git submodule update --init --recursive # Initialize the tools submodule
python tools/setup_tools.py # Add tools to settings.json file
cd tools/api_database_tools
pip install . # Install the MCP package
claude mcp add tt-metal-tools tt-metal-mcp # Register the MCP with Claude Code
cd ../..
```

#### 2. Verify

You can verify the tools are installed correctly by running the following command:

```bash
claude mcp list
```

This is the expected output:

```
Checking MCP server health...

tt-metal-tools: tt-metal-mcp  - ✓ Connected
```

#### Troubleshooting

If it can't find anything when doing `claude mcp list`, the `pip install .` command didn't work correctly.  If it can see the tools, but it can't connect, there may have been an issue with the `claude mcp add` command.
