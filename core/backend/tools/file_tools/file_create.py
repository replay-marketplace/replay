"""
File creation tool for creating new files.
"""

import logging
from typing import Dict, Any
from dataclasses import dataclass

from ..base import Tool

logger = logging.getLogger(__name__)

@dataclass
class FileCreateTool:
    """Tool to create a new file."""
    file_path: str
    content: str
    
    def execute(self, replay) -> None:
        """Execute file creation."""
        from core.backend.processors.prompt_node_processor import PromptNodeProcessor
        processor = PromptNodeProcessor()
        processor._save_generated_file(self.file_path, self.content, replay.code_dir)
        logger.info(f"Created file: {self.file_path}")
    
    @property
    def tool_name(self) -> str:
        return "file_create"
    
    @property
    def tool_description(self) -> str:
        return "Create a new file with specified content"
    
    @property
    def tool_parameters(self) -> Dict[str, Any]:
        return {
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