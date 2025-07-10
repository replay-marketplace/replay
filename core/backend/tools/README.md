# Tool System for LLM Tool Use

This system provides a clean, focused approach to handling LLM tool calls through a standardized interface that follows Anthropic's tool calling specification.

## Overview

The tool system bridges LLM responses and executable actions by detecting structured tool calls and executing them through a unified interface. Each tool represents a specific action (file creation, line editing, command execution, etc.).

## Architecture

```
LLM Response → Tool Call Detector → Tool Registry → Tool Execution
     ↓              ↓              ↓              ↓
Structured JSON  Tool Calls     Tool Classes   File/System Actions
```

## Tool Call Detection

The system detects tool calls from structured responses according to Anthropic's specification:

### 1. Anthropic Content Format
```json
{
  "content": [
    {
      "type": "tool_use",
      "name": "file_create",
      "input": {
        "file_path": "hello.py",
        "content": "print('Hello, World!')"
      }
    }
  ]
}
```

### 2. Direct Tool Calls Array
```json
{
  "tool_calls": [
    {
      "name": "file_create",
      "parameters": {
        "file_path": "test.py",
        "content": "print('Test file')"
      }
    }
  ]
}
```

### 3. Single Tool Call Object
```json
{
  "type": "tool_use",
  "name": "file_create",
  "input": {
    "file_path": "simple.py",
    "content": "print('Simple!')"
  }
}
```

### 4. JSON String Response
```json
'{"type": "tool_use", "name": "file_create", "input": {"file_path": "string.py", "content": "print(\"From string\")"}}'
```

## Available Tools

### File Operations
- `file_create`: Create a new file with content
- `file_edit_line`: Edit a specific line in a file
- `file_edit_lines`: Edit multiple lines in a file
- `file_find`: Search for content in files
- `file_replace`: Replace content in a file
- `file_remove`: Remove content from a file

### System Operations
- `command`: Execute a system command
- `tool_run`: Run a specific tool with parameters
- `memory_update`: Update memory with new information

## Usage Examples

### Simple Usage (Recommended)

```python
from core.backend.processors.prompt_node_processor import PromptNodeProcessor

processor = PromptNodeProcessor()

# LLM generates structured response with tool calls
response = {
    "content": [
        {
            "type": "tool_use",
            "name": "file_create",
            "input": {
                "file_path": "hello.py",
                "content": "print('Hello, World!')"
            }
        },
        {
            "type": "tool_use",
            "name": "command",
            "input": {
                "command": "python hello.py"
            }
        }
    ]
}

# Process the response (automatically detects tool calls)
processor.process_response(response, replay)
```

### JSON String Response

```python
# Handle JSON string response
json_response = '''
{
  "type": "tool_use",
  "name": "file_create",
  "input": {
    "file_path": "app.py",
    "content": "print('Hello from app!')"
  }
}
'''

processor.process_response(json_response, replay)
```

### Anthropic Tool Use Integration

```python
from core.backend.examples.anthropic_tool_use_example import AnthropicToolUseExample

# Initialize with Anthropic client
example = AnthropicToolUseExample("your-api-key")

# Get available tools for Anthropic
tools = example.get_anthropic_tools()

# Send request with tools enabled
response = example.send_request_with_tools(
    prompt="Create a Python function and run it",
    files=[{"path": "main.py", "content": "# Start here", "readonly": False}]
)

# Process tool calls from response
example.process_anthropic_response(response, replay)
```

## Tool Schema Example

Each tool automatically generates an Anthropic-compatible tool schema:

```json
{
  "type": "function",
  "function": {
    "name": "file_create",
    "description": "Create a new file with specified content",
    "parameters": {
      "type": "object",
      "properties": {
        "file_path": {
          "type": "string",
          "description": "Path where the file should be created"
        },
        "content": {
          "type": "string",
          "description": "Content to write to the file"
        }
      },
      "required": ["file_path", "content"]
    }
  }
}
```

## Benefits

1. **Anthropic Compliant**: Follows Anthropic's tool calling specification exactly
2. **Structured Only**: No text parsing - only handles structured JSON responses
3. **Type Safety**: Strongly typed parameters with validation
4. **Extensibility**: Easy to add new tools by implementing the Tool protocol
5. **Reliability**: Clean, predictable tool call extraction
6. **Standardization**: Aligned with modern LLM tool calling conventions

## Adding New Tools

To add a new tool:

1. Create a new class implementing the `Tool` protocol
2. Add tool metadata properties (`tool_name`, `tool_description`, `tool_parameters`)
3. Implement the `execute` method
4. Register it in the `ToolRegistry`

```python
@dataclass
class MyCustomTool:
    parameter1: str
``` 