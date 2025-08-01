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

If you want to see the tools working, or the format of output it feeds to the model, you can run the following command: 

```bash
pytest -s tools/api_database_tools/tests/test_all_tools.py --display-results
```

#### Troubleshooting

If it can't find anything when doing `claude mcp list`, the `pip install .` or `claude mcp add` command didn't work correctly.  

If it can see the tools, but it can't connect, try doing `claude mcp remove tt-metal-tools`, make sure you are in the api_database_tools directory, and paste this command exactly: `claude mcp add -- tt-metal-tools python server.py`.
