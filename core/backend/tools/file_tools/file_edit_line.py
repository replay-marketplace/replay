"""
File line editing tool for editing specific lines in files.
"""

import os
import logging
from typing import Dict, Any
from dataclasses import dataclass

from ..base import Tool

logger = logging.getLogger(__name__)

@dataclass
class FileEditLineTool:
    """Tool to edit a single line in a file."""
    file_path: str
    line_number: int
    content: str
    
    def execute(self, replay) -> None:
        """Execute single line edit."""
        file_path = os.path.join(replay.code_dir, self.file_path)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if 1 <= self.line_number <= len(lines):
                lines[self.line_number - 1] = self.content + '\n'
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                logger.info(f"Edited line {self.line_number} in {self.file_path}")
            else:
                logger.warning(f"Line number {self.line_number} out of range for {self.file_path}")
    
    @property
    def tool_name(self) -> str:
        return "file_edit_line"
    
    @property
    def tool_description(self) -> str:
        return "Edit a specific line in an existing file"
    
    @property
    def tool_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to edit"
                },
                "line_number": {
                    "type": "integer",
                    "description": "Line number to edit (1-based)"
                },
                "content": {
                    "type": "string",
                    "description": "New content for the line"
                }
            },
            "required": ["file_path", "line_number", "content"]
        } 