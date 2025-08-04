### Tool Usage Guide

Once installed, the tools will be automatically discovered and used by the Claude Code SDK when called programmatically (such as through `replay.py`). The tools work regardless of which directory you run `replay.py` from.

**Interactive Usage**: You can test the tools interactively by running `claude` from the `tools/api_database_tools` directory and asking it to test the tools. Note that interactive usage requires being in the correct directory due to the MCP server registration.

**Programmatic Usage**: The tools are designed to work seamlessly with the Claude Code SDK. By default, all tools are available when using `replay.py`. A functionality has been added to the `replay.py` script which allows you to specify which tools NOT to use. This is done by passing this flag when calling the replay script:

`--disable-tools <tool_1> <tool_2>` or `--disable-tools all`

You can also disable specific functions from the tt-metal-tools server:

`--disable-tools tt-metal-tools:decompose_function tt-metal-tools:query_llk_functions`

Available function names:
- `decompose_function`
- `query_llk_functions` 
- `find_similar_symbols`

Or, equivelently, you can disable all the tools by running the following command:

```bash
claude mcp remove tt-metal-tools
```

This won't crash the replay script, but it will disable the tools.
