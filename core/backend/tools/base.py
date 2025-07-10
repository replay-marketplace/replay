"""
Base Tool interface and types for Anthropic Tool Use integration.
"""

from typing import Protocol, Dict, Any, Optional
from abc import abstractmethod
from dataclasses import dataclass

class Tool(Protocol):
    """Interface for all tools that can be used as Anthropic Tool Use functions."""
    @abstractmethod
    def execute(self, replay) -> None:
        """Execute this tool."""
        pass
    
    @property
    @abstractmethod
    def tool_name(self) -> str:
        """Return the tool name for Anthropic."""
        pass
    
    @property
    @abstractmethod
    def tool_description(self) -> str:
        """Return the tool description for Anthropic."""
        pass
    
    @property
    @abstractmethod
    def tool_parameters(self) -> Dict[str, Any]:
        """Return the tool parameters schema for Anthropic."""
        pass

@dataclass
class ToolCall:
    """Represents a tool call that can be sent to Anthropic."""
    tool_name: str
    parameters: Dict[str, Any]
    tool: Tool 