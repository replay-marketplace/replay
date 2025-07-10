"""
Memory update tool for storing information in memory.
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

from ..base import Tool

logger = logging.getLogger(__name__)

@dataclass
class MemoryUpdateTool:
    """Tool to update memory with new information."""
    operation: str = "append"  # "append" or "get_all"
    key: Optional[str] = None
    value: Optional[str] = None
    
    def execute(self, replay) -> Any:
        """Execute memory operation."""
        if not hasattr(replay, 'memory'):
            replay.memory = {}
        
        if self.operation == "get_all":
            return self._get_all_memory(replay)
        else:  # default to "append"
            return self._append_memory(replay)
    
    def _append_memory(self, replay) -> None:
        """Append value to existing memory entry."""
        if self.key not in replay.memory:
            replay.memory[self.key] = ""
        
        current_value = replay.memory[self.key]
        if current_value:
            replay.memory[self.key] = current_value + "\n" + self.value
        else:
            replay.memory[self.key] = self.value
        
        logger.info(f"Appended to memory {self.key}")
    
    def _get_all_memory(self, replay) -> Dict[str, Any]:
        """Get all memory entries."""
        return replay.memory
    
    @property
    def tool_name(self) -> str:
        return "memory_update"
    
    @property
    def tool_description(self) -> str:
        return """        
Memory tool for storing and retrieving information.
Supports two operations:
- "append": Append to existing memory value
- "get_all": Retrieve all memory entries

Use memory tool to maintain concise summary of your responses.
Do not assume that your current action is successful until confirmed that a check was successful.
Do not save "fixed" or "resolved". I will call tests to verify if suggested change works.
Keep memory entries focused. Include any new facts you learned from our interaction.
"""
    
    @property
    def tool_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["append", "get_all"],
                    "description": "Memory operation to perform (default: append)"
                },
                "key": {
                    "type": "string",
                    "description": "Memory key (required for append operation)"
                },
                "value": {
                    "type": "string",
                    "description": "Value to store (required for append operation)"
                }
            },
            "required": ["operation"]
        } 