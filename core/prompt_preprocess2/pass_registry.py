import inspect
from typing import Callable, Dict, Any, List
from .ir.ir import EpicIR

class PassInfo:
    """Information about a registered pass."""
    
    def __init__(self, func: Callable, name: str, description: str = ""):
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
    def __init__(self):
        self._registry = {}
        self._pass_order = []
    
    def register(self, pass_func: Callable, name: str = None, description: str = None):
        """
        Register a pass function.
        
        Args:
            pass_func: Function that takes EpicIR and returns EpicIR
            name: Optional name for the pass (if not provided, will use function name without 'pass_' prefix)
            description: Optional description (if not provided, will use function's docstring)
        """
        pass_info = PassInfo(pass_func, name, description)
        # must use name from pass_info.name, which might be a generated name
        self._registry[pass_info.name] = pass_info
        self._pass_order.append(pass_info.name)
    
    def get(self, name: str) -> PassInfo:
        """Get a pass by name."""
        return self._registry.get(name)
    
    def get_all_passes(self) -> List[PassInfo]:
        """Get all registered passes in registration order."""
        return [self._registry[name] for name in self._pass_order] 