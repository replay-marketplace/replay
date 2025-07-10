"""
Prompt Node Processor for handling LLM responses with Tool Use support.
"""

import logging
from typing import List, Dict, Any, Optional, Union

from .base_processor import BaseProcessor, FileInfo

logger = logging.getLogger(__name__)

class PromptNodeProcessor(BaseProcessor):
    """Processes LLM responses with support for Tool Use."""
    
    def process(self, replay, node: dict) -> None:
        """No-op process method for PromptNodeProcessor (handled in preprocessing)."""
        logger.info("PromptNodeProcessor: no-op (handled in preprocessing)")
        return
    
    def process_response(self, response: Union[str, Dict[str, Any]], replay) -> None:
        """
        Process LLM response by detecting and executing tool calls.
        
        Args:
            response: LLM response text or structured response
            replay: Replay instance
        """
        # Extract tool calls from response
        tool_calls = self.extract_tool_calls(response)
        
        # Execute all tool calls
        results = self.execute_tool_calls(tool_calls, replay)
        
        # Log results
        for result in results:
            if result["success"]:
                logger.info(f"✅ {result['message']}")
            else:
                logger.error(f"❌ {result['error']}")
    
    def get_anthropic_tools(self, model_version: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get Anthropic tool schemas."""
        return self.get_anthropic_tools_schema()
    
    def process_anthropic_tool_call(self, tool_call: Dict[str, Any], model_version: str, replay) -> Any:
        """Process an Anthropic tool call using the appropriate tool."""
        tool_name = tool_call.get("name")
        
        # For now, fall back to custom tools since text editor tool is not implemented
        try:
            tool = self.create_tool_from_tool_call(
                tool_name, 
                tool_call.get("input", {})
            )
            tool.execute(replay)
            logger.info(f"Executed custom tool call: {tool_name}")
            return {"output": f"Successfully executed {tool_name}"}
        except Exception as e:
            logger.error(f"Error executing tool call {tool_name}: {e}")
            return {"error": str(e)} 