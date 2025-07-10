"""
Tool registry for managing Anthropic Tool Use integration.
"""

from typing import Dict, List, Type, Any
from .base import Tool, ToolCall
from .file_tools import (
    FileCreateTool, FileEditLineTool, FileEditLinesTool,
    FileFindTool, FileReplaceTool, FileRemoveTool
)
from .system_tools import CommandTool, ToolRunTool, MemoryUpdateTool
from .system_tools.api_reference_tool import APIReferenceTool

class ToolRegistry:
    """Registry for all available tools."""
    
    def __init__(self):
        self._tool_classes: Dict[str, Type[Tool]] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register all default tool classes."""
        tools = [
            # File tools
            FileCreateTool,
            FileEditLineTool,
            FileEditLinesTool,
            FileFindTool,
            FileReplaceTool,
            FileRemoveTool,
            
            # System tools
            CommandTool,
            ToolRunTool,
            MemoryUpdateTool,
            APIReferenceTool,
        ]
        
        for tool_class in tools:
            # Create a temporary instance to get the tool name
            temp_instance = tool_class.__new__(tool_class)
            tool_name = temp_instance.tool_name
            self._tool_classes[tool_name] = tool_class
    
    def get_anthropic_tools(self) -> List[Dict[str, Any]]:
        """Generate Anthropic tool schemas for all registered tools."""
        tools = []
        
        for tool_name, tool_class in self._tool_classes.items():
            # Create a temporary instance to get tool metadata
            temp_instance = tool_class.__new__(tool_class)
            
            tool_schema = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": temp_instance.tool_description,
                    "parameters": temp_instance.tool_parameters
                }
            }
            tools.append(tool_schema)
        
        return tools
    
    def create_tool_from_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Tool:
        """Create a tool instance from a tool call."""
        if tool_name not in self._tool_classes:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        tool_class = self._tool_classes[tool_name]
        
        # Handle special cases for parameter mapping
        if tool_name == "file_edit_lines":
            # Convert start_line/end_line to line_range tuple
            start_line = parameters.get("start_line")
            end_line = parameters.get("end_line")
            if start_line is not None and end_line is not None:
                parameters["line_range"] = (start_line, end_line)
                parameters.pop("start_line", None)
                parameters.pop("end_line", None)
        
        elif tool_name == "file_remove":
            # Convert start_line/end_line to line_range tuple if both provided
            start_line = parameters.get("start_line")
            end_line = parameters.get("end_line")
            if start_line is not None and end_line is not None:
                parameters["line_range"] = (start_line, end_line)
                parameters.pop("start_line", None)
                parameters.pop("end_line", None)
        
        return tool_class(**parameters)
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return list(self._tool_classes.keys())
    
    def register_tool(self, tool_name: str, tool_class: Type[Tool]):
        """Register a new tool class."""
        self._tool_classes[tool_name] = tool_class

# Global registry instance
tool_registry = ToolRegistry() 