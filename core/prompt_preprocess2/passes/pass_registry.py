import inspect
from typing import Callable, Dict, Any, List
from ..ir.ir import EpicIR

class PassInfo:
    """
    Information about a registered preprocessing pass.
    
    The PassInfo class encapsulates metadata about a pass function, including
    the function itself, its name, and description. This allows the pass registry
    to maintain organized information about available passes.
    
    Attributes:
        func (Callable): The pass function that transforms EpicIR
        name (str): The display name of the pass
        description (str): A description of what the pass does
    """
    
    def __init__(self, func: Callable, name: str, description: str = ""):
        """
        Initialize pass information.
        
        Args:
            func (Callable): Function that takes EpicIR and returns EpicIR
            name (str): Name for the pass (auto-generated if empty)
            description (str): Description of the pass (uses docstring if empty)
        """
        self.func = func
        self.name = name

        # Auto-generate name from function name if not provided                
        # Generate name from function name if not provided        
        if name is None or name == "": 
            func_name = func.__name__
            if func_name.startswith('pass_'):
                self.name = func_name[5:]  # Remove 'pass_' prefix
            else:
                self.name = func_name
        # Use provided description or extract from function docstring
        self.description = description or (func.__doc__ or "").strip()

class PassRegistry:
    """
    Registry for managing preprocessing passes in the prompt preprocessing pipeline.
    
    The PassRegistry maintains an ordered collection of passes that transform the
    intermediate representation (EpicIR) during prompt preprocessing. Passes are
    executed in registration order to progressively transform the graph structure.
    
    Common passes include:
    - Lowering high-level constructs to primitive operations
    - Inserting control flow nodes
    - Processing file references and markers
    - Optimizing graph structure
    
    Example:
        registry = PassRegistry()
        registry.register(pass_lower_debug_loop)
        registry.register(pass_insert_exit_node)
        
        for pass_info in registry.get_all_passes():
            epic = pass_info.func(epic)
    """
    
    def __init__(self):
        """Initialize an empty pass registry."""
        self._registry = {}
        self._pass_order = []
    
    def register(self, pass_func: Callable, name: str = None, description: str = None) -> None:
        """
        Register a pass function in the registry.
        
        Args:
            pass_func (Callable): Function that takes EpicIR and returns EpicIR
            name (str, optional): Name for the pass (auto-generated if not provided)
            description (str, optional): Description (uses function docstring if not provided)
        """
        pass_info = PassInfo(pass_func, name, description)
        # must use name from pass_info.name, which might be a generated name
        self._registry[pass_info.name] = pass_info
        self._pass_order.append(pass_info.name)
    
    def get(self, name: str) -> PassInfo:
        """
        Get a pass by name.
        
        Args:
            name (str): The name of the pass to retrieve
            
        Returns:
            PassInfo: The pass information, or None if not found
        """
        return self._registry.get(name)
    
    def get_all_passes(self) -> List[PassInfo]:
        """
        Get all registered passes in registration order.
        
        Returns:
            List[PassInfo]: All registered passes in the order they were registered
        """
        return [self._registry[name] for name in self._pass_order] 