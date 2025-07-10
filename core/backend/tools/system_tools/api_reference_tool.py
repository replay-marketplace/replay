"""
API Reference Tool for providing API documentation and examples.
"""

import logging
from typing import Dict, Any
from dataclasses import dataclass

from ..base import Tool

logger = logging.getLogger(__name__)

@dataclass
class APIReferenceTool:
    """Tool to get API reference information."""
    api_name: str
    
    def execute(self, replay) -> None:
        """Get API reference and add to memory."""
        try:
            api_reference = self._get_api_reference(self.api_name)
            
            # Add to memory
            memory_entry = f"API Reference for {self.api_name}: {api_reference}"
            replay.state.execution.memory.append(memory_entry)
            
            logger.info(f"Added API reference for {self.api_name} to memory")
            
        except Exception as e:
            logger.error(f"Error getting API reference for {self.api_name}: {e}")
    
    def _get_api_reference(self, api_name: str) -> str:
        """Get the API reference for a given API name."""
        # This is a mock implementation - in a real system, this would query
        # an actual API database or documentation system
        
        api_references = {
            "sfpu_reciprocal": """
## SFPU Reciprocal Function
Use `ckernel::sfpu::_sfpu_reciprocal_(val)` instead of `1.0f / val`

Example:
```cpp
// Instead of: result = (1.0f / val) * other_val;
sfpi::vFloat result = ckernel::sfpu::_sfpu_reciprocal_(val) * other_val;
```
""",
            "vFloat": """
## vFloat Type
Use `sfpi::vFloat` for vector float operations.

Example:
```cpp
// For constants:
sfpi::vFloat one = sfpi::vFloat(1.0f);  // Convert to vFloat first
sfpi::vFloat result = one / val;  // Now safe to divide
```
""",
            "include": """
## Header Include Issues
If you get an error like "No such file or directory" for an include - remove this include.

Common fixes:
- Remove unused includes
- Use correct include paths
- Check for typos in header names
""",
            "operator": """
## Operator Issues
For operator-related errors, ensure proper type handling:

```cpp
// Instead of: result = (1.0f / val) * other_val;
sfpi::vFloat result = ckernel::sfpu::_sfpu_reciprocal_(val) * other_val;

// Or for constants:
sfpi::vFloat one = sfpi::vFloat(1.0f);  // Convert to vFloat first
```
""",
            "default": """
## General API Reference
For API-related issues:
1. Check include statements
2. Verify function signatures
3. Ensure proper type conversions
4. Use SFPU functions for vector operations
"""
        }
        
        # Try to find a specific reference, fall back to default
        for key, reference in api_references.items():
            if key.lower() in api_name.lower():
                return reference
        
        return api_references["default"]
    
    @property
    def tool_name(self) -> str:
        return "get_api_reference"
    
    @property
    def tool_description(self) -> str:
        return """Retrieves comprehensive API reference documentation and usage examples for a given API name or header. This tool should be used when encountering compilation errors related to unknown APIs, missing includes, or incorrect API usage patterns. It provides specific guidance on how to fix common issues like operator errors, include problems, and type conversion issues. The tool returns detailed examples showing the correct way to use APIs, alternative approaches, and best practices for the specific programming context. Use this tool whenever you need to understand how to properly use an API that's causing compilation or runtime errors."""
    
    @property
    def tool_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                            "api_name": {
                "type": "string",
                "description": "The name of the API, function, header, or operator to get reference documentation for. This can be a function name like 'sfpu_reciprocal', a type like 'vFloat', an operator like 'operator/', or a header name like 'iostream'. The tool will search for the most relevant documentation and examples for the specified API."
            }
            },
            "required": ["api_name"]
        } 