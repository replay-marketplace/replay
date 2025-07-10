# FixNodeProcessor Update: XML Format and Anthropic Tool Use

## Overview

The `FixNodeProcessor` has been updated to use the new XML format and proper Anthropic tool use approach for LLM communication. This update follows the official Anthropic tool use specification and provides better integration with the tool system.

## Key Changes

### 1. XML Format Integration

**Before**: Used JSON format for LLM communication
```python
# Old approach
request_dict = {
    "prompt": llm_request.prompt,
    "run_logs_files": [{"path_and_filename": f.path, "contents": f.content} for f in llm_request.run_logs_files],
    "code_to_edit": [{"path_and_filename": f.path, "contents": f.content} for f in llm_request.code_to_edit],
    "memory": llm_request.memory
}
request_json = json.dumps(request_dict, indent=2)
```

**After**: Uses XML format with semantic tags
```python
# New approach
def _build_xml_request(self, llm_request: LLMRequest) -> str:
    xml_parts = []
    
    # Add code files to edit (no readonly attribute)
    if llm_request.code_to_edit:
        for file_ref in llm_request.code_to_edit:
            xml_parts.append(f'<file path="{file_ref.path}">')
            xml_parts.append(self._escape_xml(file_ref.content))
            xml_parts.append('</file>')
    
    # Add read-only files (with readonly flag)
    if llm_request.read_only_files:
        for file_ref in llm_request.read_only_files:
            xml_parts.append(f'<file path="{file_ref.path}" readonly>')
            xml_parts.append(self._escape_xml(file_ref.content))
            xml_parts.append('</file>')
    
    # Add memory
    if llm_request.memory:
        xml_parts.append('<memory>')
        for entry in llm_request.memory:
            xml_parts.append(f'<entry>{self._escape_xml(entry)}</entry>')
        xml_parts.append('</memory>')
    
    return '\n'.join(xml_parts)
```

### 2. Proper Anthropic Tool Use Implementation

**Before**: Manual tool call extraction from text
```python
# Old approach - parsing text for tool calls
def _extract_tool_calls(self, response: str) -> List[Dict[str, Any]]:
    # Complex regex parsing of text responses
    json_pattern = r'```json\s*(\{.*?\})\s*```'
    tool_pattern = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
    # ... manual parsing logic
```

**After**: Proper Anthropic tool use handling
```python
# New approach - proper tool use handling
def _process_llm_response(self, response, replay) -> None:
    if response.stop_reason == "tool_use":
        self._handle_tool_use_response(response, replay)
    else:
        # Handle regular response with XML parsing
        response_content = response.content[0].text if response.content else ""
        # ... XML parsing logic

def _handle_tool_use_response(self, response, replay) -> None:
    tool_results = []
    
    for content_block in response.content:
        if content_block.type == "tool_use":
            try:
                tool = self.tool_registry.create_tool_from_tool_call(
                    content_block.name, 
                    content_block.input
                )
                tool.execute(replay)
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": content_block.id,
                    "content": f"Successfully executed {content_block.name}"
                })
            except Exception as e:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": content_block.id,
                    "content": f"Error executing {content_block.name}: {str(e)}",
                    "is_error": True
                })
    
    if tool_results:
        self._continue_with_tool_results(response, tool_results, replay)
```

### 3. Tool Schema Generation

**Before**: Used tool registry's basic schema
```python
# Old approach
tools = self.tool_registry.get_anthropic_tools()
```

**After**: Proper Anthropic tool schema format
```python
# New approach
def _get_anthropic_tools_schema(self) -> List[Dict[str, Any]]:
    tools = []
    
    for tool_name in self.tool_registry.get_available_tools():
        try:
            tool = self.tool_registry.create_tool_from_tool_call(tool_name, {})
            
            tool_schema = {
                "name": tool.tool_name,
                "description": tool.tool_description,
                "input_schema": tool.tool_parameters
            }
            tools.append(tool_schema)
        except Exception as e:
            logger.warning(f"Could not create schema for tool {tool_name}: {e}")
    
    return tools
```

### 4. New API Reference Tool

Created a dedicated tool for API reference lookups:

```python
@dataclass
class APIReferenceTool:
    """Tool to get API reference information."""
    api_name: str
    
    def execute(self, replay) -> None:
        api_reference = self._get_api_reference(self.api_name)
        memory_entry = f"API Reference for {self.api_name}: {api_reference}"
        replay.state.execution.memory.append(memory_entry)
    
    @property
    def tool_description(self) -> str:
        return """Retrieves comprehensive API reference documentation and usage examples for a given API name or header. This tool should be used when encountering compilation errors related to unknown APIs, missing includes, or incorrect API usage patterns. It provides specific guidance on how to fix common issues like operator errors, include problems, and type conversion issues. The tool returns detailed examples showing the correct way to use APIs, alternative approaches, and best practices for the specific programming context. Use this tool whenever you need to understand how to properly use an API that's causing compilation or runtime errors."""
```

## Benefits of the Update

### 1. **Proper Tool Use Handling**
- Follows Anthropic's official tool use specification
- Handles `tool_use` stop_reason correctly
- Proper conversation continuation with tool results
- Error handling for tool execution failures

### 2. **XML Format Advantages**
- Semantic meaning in tags (`<file>`, `<memory>`, `<edit>`)
- Clear distinction between editable and read-only files
- Better structure for complex file operations
- Line number support for precise edits

### 3. **Enhanced Tool System**
- Dedicated API reference tool with comprehensive descriptions
- Proper tool schema generation
- Better error handling and logging
- Integration with the existing tool registry

### 4. **Improved LLM Communication**
- Uses proper Anthropic tool schemas
- Supports parallel tool use
- Better prompting for tool usage
- Fallback to JSON parsing for compatibility

## Usage Example

```python
# The processor now handles both XML and tool use seamlessly
processor = FixNodeProcessor()

# Process a FIX node
processor.process(replay, node)

# The processor will:
# 1. Send XML-formatted request with tools enabled
# 2. Handle tool_use responses properly
# 3. Continue conversation with tool results
# 4. Parse XML responses for file operations
# 5. Fall back to JSON if needed
```

## Configuration

The processor now uses:
- `CLIENT_INSTRUCTIONS_FILE = "client_instructions_with_xml.txt"` for XML format
- Proper tool schemas for Anthropic API
- Enhanced error handling and logging
- Memory management for tool results

## Backward Compatibility

The update maintains backward compatibility by:
- Falling back to JSON parsing if XML parsing fails
- Supporting both old and new tool call formats
- Maintaining the same public API
- Preserving existing functionality

## Testing

Use the provided test files:
- `test_fix_node_processor.py` - Basic functionality test
- `example_fix_node_processor_usage.py` - Comprehensive demonstration

The examples show how the processor now properly handles:
1. Tool use requests from the LLM
2. Tool execution and result handling
3. Conversation continuation
4. XML response parsing
5. Error handling and logging 