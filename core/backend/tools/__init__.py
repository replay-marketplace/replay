"""
Tool system for Anthropic Tool Use integration.

This package provides a modular tool system that can be used with both
XML parsing and Anthropic Tool Use for executing file and system operations.
"""

from .base import Tool, ToolCall
from .tool_registry import tool_registry, ToolRegistry

# Import all tools
from .file_tools import (
    FileCreateTool,
    FileEditLineTool,
    FileEditLinesTool,
    FileFindTool,
    FileReplaceTool,
    FileRemoveTool
)

from .system_tools import (
    CommandTool,
    ToolRunTool,
    MemoryUpdateTool,
    APIReferenceTool
)

__all__ = [
    # Base classes
    'Tool',
    'ToolCall',
    'ToolRegistry',
    'tool_registry',
    
    # File tools
    'FileCreateTool',
    'FileEditLineTool',
    'FileEditLinesTool',
    'FileFindTool',
    'FileReplaceTool',
    'FileRemoveTool',
    
    # System tools
    'CommandTool',
    'ToolRunTool',
    'MemoryUpdateTool',
    'APIReferenceTool',
] 