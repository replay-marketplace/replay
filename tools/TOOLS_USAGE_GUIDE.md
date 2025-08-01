### Tool Usage Guide

Once installed, the tools will be automatically discovered by Claude Code and available to use, you can verify this by calling `claude` from the terminal and asking it to test out the tools. 

The tools need to be specifically configured when using the Claude Code SDK calls for programmatic use. By default, all the tools are be available to use.  A functionality has been added to the `replay.py` script which allows you to specify which tools NOT to use. This is done by passing this flag when calling the replay script:

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
