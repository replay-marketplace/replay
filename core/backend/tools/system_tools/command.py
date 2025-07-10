"""
System command execution tool for running shell commands.
"""

import subprocess
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

from ..base import Tool

logger = logging.getLogger(__name__)

@dataclass
class CommandTool:
    """Tool to execute a system command."""
    command: str
    cwd: Optional[str] = None
    
    def execute(self, replay) -> None:
        """Execute system command."""
        try:
            working_dir = self.cwd or replay.code_dir
            result = subprocess.run(
                self.command,
                shell=True,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info(f"Command executed successfully: {self.command}")
                if result.stdout:
                    logger.info(f"Output: {result.stdout}")
            else:
                logger.warning(f"Command failed: {self.command}")
                if result.stderr:
                    logger.warning(f"Error: {result.stderr}")
                    
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {self.command}")
        except Exception as e:
            logger.error(f"Error executing command {self.command}: {e}")
    
    @property
    def tool_name(self) -> str:
        return "command"
    
    @property
    def tool_description(self) -> str:
        return "Execute a system command"
    
    @property
    def tool_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to execute"
                },
                "cwd": {
                    "type": "string",
                    "description": "Working directory for the command (optional)"
                }
            },
            "required": ["command"]
        } 