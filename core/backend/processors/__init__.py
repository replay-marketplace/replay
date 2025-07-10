"""
Processors for handling different types of nodes and LLM responses.
"""

from .base_processor import BaseProcessor, FileReference, FileInfo
from .fix_node_processor import FixNodeProcessor
from .prompt_node_processor import PromptNodeProcessor
from .registry import NodeProcessorRegistry

__all__ = [
    'BaseProcessor',
    'FileReference', 
    'FileInfo',
    'FixNodeProcessor',
    'PromptNodeProcessor',
    'NodeProcessorRegistry',
] 