"""
Base processor class for common LLM processing functionality.
"""

import json
import logging
import os
from typing import Dict, List, Any, Union, Optional
from dataclasses import dataclass

from ..tools import tool_registry

logger = logging.getLogger(__name__)

@dataclass
class FileReference:
    """Represents a file reference with path and content."""
    path: str
    content: str

@dataclass
class FileInfo:
    """Information about a file for context."""
    path: str
    content: str
    readonly: bool = False
    line_numbers: bool = True

class BaseProcessor:
    """Base class for LLM processors with common tool handling functionality."""
    
    def __init__(self):
        self.tool_registry = tool_registry
    
    # ============================================================================
    # Tool Registry Integration
    # ============================================================================
    
    def create_tool_from_tool_call(self, tool_name: str, parameters: Dict[str, Any]):
        """Create a tool instance from a tool call."""
        return self.tool_registry.create_tool_from_tool_call(tool_name, parameters)
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return self.tool_registry.get_available_tools()
    
    def get_anthropic_tools_schema(self) -> List[Dict[str, Any]]:
        """Get tools in proper Anthropic schema format."""
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
    
    # ============================================================================
    # Tool Execution
    # ============================================================================
    
    def execute_tool_call(self, tool_name: str, parameters: Dict[str, Any], replay) -> Dict[str, Any]:
        """Execute a single tool call and return result."""
        try:
            tool = self.create_tool_from_tool_call(tool_name, parameters)
            tool.execute(replay)
            logger.info(f"Executed tool call: {tool_name}")
            return {
                "success": True,
                "tool_name": tool_name,
                "message": f"Successfully executed {tool_name}"
            }
        except Exception as e:
            logger.error(f"Error executing tool call {tool_name}: {e}")
            return {
                "success": False,
                "tool_name": tool_name,
                "error": str(e)
            }
    
    def execute_tool_calls(self, tool_calls: List[Dict[str, Any]], replay) -> List[Dict[str, Any]]:
        """Execute multiple tool calls and return results."""
        results = []
        for tool_call in tool_calls:
            result = self.execute_tool_call(
                tool_call["name"], 
                tool_call["parameters"], 
                replay
            )
            results.append(result)
        return results
    
    # ============================================================================
    # Tool Call Extraction
    # ============================================================================
    
    def extract_tool_calls(self, response: Union[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract tool calls from structured response according to Anthropic specification."""
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError:
                logger.warning("Response is a string but not valid JSON. No tool calls found.")
                return []
        
        return self._extract_tool_calls_from_structured(response)
    
    def _extract_tool_calls_from_structured(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract tool calls from structured response (Anthropic format)."""
        tool_calls = []
        
        # Handle Anthropic format with content array
        if "content" in response:
            for content_item in response["content"]:
                if content_item.get("type") == "tool_use":
                    tool_calls.append({
                        "name": content_item.get("name", ""),
                        "parameters": content_item.get("input", {})
                    })
        
        # Handle direct tool_calls array
        elif "tool_calls" in response:
            for tool_call in response["tool_calls"]:
                tool_calls.append({
                    "name": tool_call.get("name", ""),
                    "parameters": tool_call.get("parameters", {})
                })
        
        # Handle single tool call object
        elif response.get("type") == "tool_use":
            tool_calls.append({
                "name": response.get("name", ""),
                "parameters": response.get("input", {})
            })
        
        return tool_calls
    
    # ============================================================================
    # XML Formatting
    # ============================================================================
    
    def escape_xml(self, text: str) -> str:
        """Escape XML special characters."""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
    
    def format_files_for_context(self, files: List[FileInfo]) -> str:
        """Format files for LLM context with XML tags."""
        context_parts = []
        
        for file_info in files:
            if file_info.readonly:
                # Read-only files (docs, etc.)
                context_parts.append(f'<file path="{file_info.path}" readonly="true">')
                context_parts.append(self.escape_xml(file_info.content))
                context_parts.append('</file>')
            else:
                # Editable code files with line numbers
                if file_info.line_numbers:
                    lines = file_info.content.split('\n')
                    numbered_lines = []
                    for i, line in enumerate(lines, 1):
                        numbered_lines.append(f"{i:3d}: {line}")
                    content = '\n'.join(numbered_lines)
                else:
                    content = file_info.content
                
                context_parts.append(f'<file path="{file_info.path}">')
                context_parts.append(self.escape_xml(content))
                context_parts.append('</file>')
        
        return '\n'.join(context_parts)
    
    def build_xml_request(self, files: List[FileReference], memory: List[str] = None) -> str:
        """Build XML format request for LLM using semantic tags."""
        xml_parts = []
        
        # Add files
        for file_ref in files:
            xml_parts.append(f'<file path="{file_ref.path}">')
            xml_parts.append(self.escape_xml(file_ref.content))
            xml_parts.append('</file>')
        
        # Add memory
        if memory:
            xml_parts.append('<memory>')
            for entry in memory:
                xml_parts.append(f'<entry>{self.escape_xml(entry)}</entry>')
            xml_parts.append('</memory>')
        
        return '\n'.join(xml_parts)
    
    # ============================================================================
    # File Operations
    # ============================================================================
    
    def read_file_safely(self, file_path: str, last_n_lines: int = None) -> str:
        """Read a file safely with proper encoding handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if last_n_lines is not None:
                    return '\n'.join(f.readlines()[-last_n_lines:])
                else:
                    return f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return ""
    
    def save_generated_file(self, file_path: str, content: str, code_dir: str) -> None:
        """Save a generated file."""
        full_path = os.path.join(code_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # ============================================================================
    # Memory Operations
    # ============================================================================
    
    def store_in_memory(self, replay, key: str, value: str) -> bool:
        """Store a value in memory using the memory_update tool."""
        try:
            tool = self.create_tool_from_tool_call(
                "memory_update",
                {
                    "operation": "append",
                    "key": key,
                    "value": value
                }
            )
            tool.execute(replay)
            logger.info(f"Stored in memory: {key}")
            return True
        except Exception as e:
            logger.error(f"Error storing in memory: {e}")
            return False
    
    # ============================================================================
    # Anthropic Tool Use Handling
    # ============================================================================
    
    def handle_tool_use_response(self, response, replay, conversation_history=None) -> List[Dict[str, Any]]:
        """Handle tool use response according to Anthropic specification."""
        tool_results = []
        
        # Extract all tool use blocks
        for content_block in response.content:
            if content_block.type == "tool_use":
                try:
                    # Execute the tool
                    tool = self.create_tool_from_tool_call(
                        content_block.name, 
                        content_block.input
                    )
                    tool.execute(replay)
                    logger.info(f"Executed tool call: {content_block.name}")
                    
                    # Create tool result
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": f"Successfully executed {content_block.name}"
                    })
                    
                except Exception as e:
                    logger.error(f"Error executing tool call {content_block.name}: {e}")
                    # Return error result
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": f"Error executing {content_block.name}: {str(e)}",
                        "is_error": True
                    })
        
        return tool_results 