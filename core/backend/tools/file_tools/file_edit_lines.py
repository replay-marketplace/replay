"""
File multi-line editing tool for editing multiple lines in files.
"""

import os
import logging
from typing import Dict, Any, Tuple
from dataclasses import dataclass

from ..base import Tool

logger = logging.getLogger(__name__)

@dataclass
class FileEditLinesTool:
    """Tool to edit multiple lines in a file."""
    file_path: str
    line_range: Tuple[int, int]
    content: str
    
    def execute(self, replay) -> None:
        """Execute multiple line edit."""
        file_path = os.path.join(replay.code_dir, self.file_path)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            start_line, end_line = self.line_range
            if 1 <= start_line <= end_line <= len(lines):
                content_lines = self.content.split('\n')
                lines[start_line-1:end_line] = [line + '\n' for line in content_lines]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                logger.info(f"Edited lines {start_line}-{end_line} in {self.file_path}")
            else:
                logger.warning(f"Line range {start_line}-{end_line} out of range for {self.file_path}")
    
    @property
    def tool_name(self) -> str:
        return "file_edit_lines"
    
    @property
    def tool_description(self) -> str:
        return "Edit multiple lines in an existing file"
    
    @property
    def tool_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to edit"
                },
                "start_line": {
                    "type": "integer",
                    "description": "Starting line number (1-based)"
                },
                "end_line": {
                    "type": "integer",
                    "description": "Ending line number (1-based)"
                },
                "content": {
                    "type": "string",
                    "description": "New content for the lines"
                }
            },
            "required": ["file_path", "start_line", "end_line", "content"]
        } 