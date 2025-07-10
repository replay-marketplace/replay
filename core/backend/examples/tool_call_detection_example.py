"""
Example of the simplified tool call detection system.
"""

from typing import Dict, Any, List
from ..processors.prompt_node_processor import PromptNodeProcessor

class ToolCallDetectionExample:
    """Example of how the simplified tool call detection works."""
    
    def __init__(self):
        self.processor = PromptNodeProcessor()
    
    def demonstrate_tool_call_formats(self):
        """Demonstrate different tool call formats that can be detected."""
        
        # Example 1: JSON tool call format
        json_response = '''
I'll help you create a Python file and run it.

```json
{
  "type": "tool_use",
  "name": "file_create",
  "input": {
    "file_path": "hello.py",
    "content": "print('Hello, World!')"
  }
}
```

Now let's run it:

```json
{
  "type": "tool_use", 
  "name": "command",
  "input": {
    "command": "python hello.py"
  }
}
```
'''
        
        # Example 2: Function call format
        func_response = '''
Let me create a file and run a command:

```function
file_create(
  "file_path": "test.py",
  "content": "print('Test file')"
)
```

```function
command(
  "command": "python test.py"
)
```
'''
        
        # Example 3: Simple tool call format
        simple_response = '''
I'll create a file and run it:

TOOL_CALL: file_create(file_path="simple.py", content="print('Simple!')")
TOOL_CALL: command(command="python simple.py")
'''
        
        # Example 4: Mixed format
        mixed_response = '''
Let me help you with this:

```json
{
  "type": "tool_use",
  "name": "file_create",
  "input": {
    "file_path": "mixed.py",
    "content": "print('Mixed format')"
  }
}
```

And run it:

TOOL_CALL: command(command="python mixed.py")
'''
        
        # Example 5: Structured response (like from Anthropic)
        structured_response = {
            "content": [
                {
                    "type": "text",
                    "text": "I'll create a file for you."
                },
                {
                    "type": "tool_use",
                    "name": "file_create",
                    "input": {
                        "file_path": "structured.py",
                        "content": "print('From structured response')"
                    }
                },
                {
                    "type": "tool_use",
                    "name": "command",
                    "input": {
                        "command": "python structured.py"
                    }
                }
            ]
        }
        
        # Process each example
        examples = [
            ("JSON Format", json_response),
            ("Function Format", func_response),
            ("Simple Format", simple_response),
            ("Mixed Format", mixed_response),
            ("Structured Format", structured_response)
        ]
        
        for name, response in examples:
            print(f"\n=== {name} ===")
            tool_calls = self._extract_tool_calls(response)
            print(f"Detected {len(tool_calls)} tool calls:")
            for i, tool_call in enumerate(tool_calls, 1):
                print(f"  {i}. {tool_call['name']}({tool_call['parameters']})")
    
    def _extract_tool_calls(self, response) -> List[Dict[str, Any]]:
        """Extract tool calls from response using the processor."""
        return self.processor._extract_tool_calls(response)
    
    def demonstrate_parameter_parsing(self):
        """Demonstrate parameter parsing capabilities."""
        
        test_cases = [
            # Simple key=value
            'file_path="test.py", content="print(\'hello\')"',
            
            # With numbers and booleans
            'line_number=5, content="new line", enabled=true',
            
            # With nested structures
            'parameters={"nested": "value", "array": [1, 2, 3]}',
            
            # Complex nested
            'config={"timeout": 30, "retries": 3, "enabled": true}',
            
            # Mixed types
            'name="test", count=5, active=true, data={"key": "value"}'
        ]
        
        print("\n=== Parameter Parsing Examples ===")
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Input: {test_case}")
            params = self.processor._parse_key_value_params(test_case)
            print(f"   Parsed: {params}")
    
    def demonstrate_full_workflow(self):
        """Demonstrate a complete workflow with tool calls."""
        
        # Simulate a replay object
        class MockReplay:
            def __init__(self):
                self.code_dir = "/tmp/test"
                self.memory = {}
        
        replay = MockReplay()
        
        # Example LLM response with multiple tool calls
        response = '''
I'll help you set up a Python project:

First, let me create a main file:

```json
{
  "type": "tool_use",
  "name": "file_create",
  "input": {
    "file_path": "main.py",
    "content": "def greet(name):\\n    print(f'Hello, {name}!')\\n\\nif __name__ == '__main__':\\n    greet('World')"
  }
}
```

Now let's create a requirements file:

TOOL_CALL: file_create(file_path="requirements.txt", content="requests==2.31.0")

Let's run the main file:

```function
command(
  "command": "python main.py"
)
```

And update our memory:

```json
{
  "type": "tool_use",
  "name": "memory_update",
  "input": {
    "key": "project_setup",
    "value": "Created main.py and requirements.txt",
    "memory_type": "project"
  }
}
```
'''
        
        print("\n=== Full Workflow Example ===")
        print("Processing LLM response with tool calls...")
        
        # Process the response (no mode parameter needed)
        self.processor.process_response(response, replay)
        
        print("Workflow completed!")
        print(f"Memory: {replay.memory}")
    
    def demonstrate_simple_usage(self):
        """Demonstrate the simplified usage without mode parameters."""
        
        # Example 1: Text response with tool calls
        text_response = '''
I'll create a simple Python script:

TOOL_CALL: file_create(file_path="script.py", content="print('Hello from script!')")
TOOL_CALL: command(command="python script.py")
'''
        
        # Example 2: Structured response
        structured_response = {
            "tool_calls": [
                {
                    "name": "file_create",
                    "parameters": {
                        "file_path": "structured.py",
                        "content": "print('From structured response')"
                    }
                }
            ]
        }
        
        print("\n=== Simplified Usage Examples ===")
        
        # Process text response
        print("1. Processing text response:")
        tool_calls = self._extract_tool_calls(text_response)
        print(f"   Detected {len(tool_calls)} tool calls")
        
        # Process structured response
        print("2. Processing structured response:")
        tool_calls = self._extract_tool_calls(structured_response)
        print(f"   Detected {len(tool_calls)} tool calls")

def main():
    """Run the tool call detection examples."""
    example = ToolCallDetectionExample()
    
    print("🔧 Simplified Tool Call Detection Examples")
    print("=" * 50)
    
    # Demonstrate different formats
    example.demonstrate_tool_call_formats()
    
    # Demonstrate parameter parsing
    example.demonstrate_parameter_parsing()
    
    # Demonstrate simplified usage
    example.demonstrate_simple_usage()
    
    # Demonstrate full workflow
    example.demonstrate_full_workflow()
    
    print("\n✅ All examples completed!")
    print("\n💡 Key Benefits:")
    print("   - No mode parameter needed")
    print("   - Automatic tool call detection")
    print("   - Multiple format support")
    print("   - Cleaner, simpler API")

if __name__ == "__main__":
    main() 