"""
Example of using the Intent system with Anthropic Tool Use.
"""

import anthropic
from typing import Dict, Any, List

from ..tools import tool_registry
from ..processors.prompt_node_processor import PromptNodeProcessor

class AnthropicToolUseExample:
    """Example of integrating intents with Anthropic tool calling."""
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.processor = PromptNodeProcessor()
    
    def get_tools_for_anthropic(self) -> List[Dict[str, Any]]:
        """Get tool schemas for Anthropic."""
        return self.processor.get_anthropic_tools()
    
    def send_request_with_tools(self, prompt: str, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Send a request to Anthropic with tool calling enabled."""
        
        # Format files for context
        file_context = self._format_files_context(files)
        
        # Get available tools
        tools = self.get_tools_for_anthropic()
        
        # Send request to Anthropic
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            system="You are a helpful coding assistant. Use the available tools to help with file operations and system commands.",
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}\n\n{file_context}"
                }
            ],
            tools=tools
        )
        
        return response.model_dump()
    
    def _format_files_context(self, files: List[Dict[str, Any]]) -> str:
        """Format files for context."""
        context_parts = []
        
        for file_info in files:
            if file_info.get("readonly", False):
                context_parts.append(f'<file path="{file_info["path"]}" readonly="true">')
                context_parts.append(file_info["content"])
                context_parts.append('</file>')
            else:
                # Add line numbers for editable files
                lines = file_info["content"].split('\n')
                numbered_lines = []
                for i, line in enumerate(lines, 1):
                    numbered_lines.append(f"{i:3d}: {line}")
                content = '\n'.join(numbered_lines)
                
                context_parts.append(f'<file path="{file_info["path"]}">')
                context_parts.append(content)
                context_parts.append('</file>')
        
        return '\n'.join(context_parts)
    
    def process_anthropic_response(self, response: Dict[str, Any], replay) -> None:
        """Process Anthropic response and execute tool calls."""
        self.processor.process_response(response, replay, mode="anthropic")

# Example usage
def example_usage():
    """Example of how to use the Anthropic tool calling system."""
    
    # Initialize the example
    example = AnthropicToolUseExample("your-api-key-here")
    
    # Example files
    files = [
        {
            "path": "main.py",
            "content": "print('Hello, World!')\n# Add more functionality here",
            "readonly": False
        },
        {
            "path": "README.md",
            "content": "# My Project\n\nThis is a sample project.",
            "readonly": True
        }
    ]
    
    # Example prompt
    prompt = """
    Please help me improve the main.py file:
    1. Add a function to calculate the sum of two numbers
    2. Add error handling to the existing code
    3. Run the code to test it
    """
    
    # Send request with tools
    response = example.send_request_with_tools(prompt, files)
    
    # Process the response (this would execute the tool calls)
    # example.process_anthropic_response(response, replay)
    
    print("Available tools:")
    for tool in example.get_tools_for_anthropic():
        print(f"- {tool['function']['name']}: {tool['function']['description']}")

if __name__ == "__main__":
    example_usage() 