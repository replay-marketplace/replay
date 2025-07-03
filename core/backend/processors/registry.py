from .template_node_processor import TemplateNodeProcessor
from .prompt_node_processor import PromptNodeProcessor
from .run_node_processor import RunNodeProcessor
from .exit_node_processor import ExitNodeProcessor
from .doc_node_processor import DocNodeProcessor
from .conditional_node_processor import ConditionalNodeProcessor
from .fix_node_processor import FixNodeProcessor

from core.prompt_preprocess2.ir.ir import Opcode

class NodeProcessorRegistry:
    """
    Registry for managing node processors in the replay system.
    
    The NodeProcessorRegistry maps different operation codes (opcodes) to their corresponding
    processor implementations. This allows the replay system to dispatch processing of different
    node types to the appropriate handlers during execution.
    
    The registry follows a factory pattern where processors are registered once and retrieved
    as needed during execution. Each processor is responsible for handling a specific type of
    operation (PROMPT, RUN, CONDITIONAL, etc.).
    
    Example:
        registry = NodeProcessorRegistry.create_registry()
        processor = registry.get(Opcode.PROMPT)
        processor.process(replay, node)
    """
    
    def __init__(self):
        """Initialize an empty processor registry."""
        self._registry = {}
    
    def register(self, opcode: Opcode, processor) -> None:
        """
        Register a processor for a specific opcode.
        
        Args:
            opcode (Opcode): The operation code that this processor handles
            processor: The processor instance that will handle nodes of this type
        """
        self._registry[opcode] = processor
    
    def get(self, opcode: Opcode):
        """
        Retrieve the processor for a given opcode.
        
        Args:
            opcode (Opcode): The operation code to get a processor for
            
        Returns:
            The processor instance for the given opcode, or None if not registered
        """
        return self._registry.get(opcode)

    @classmethod
    def create_registry(cls) -> 'NodeProcessorRegistry':
        """
        Create a registry with all standard node processors registered.
        
        This factory method creates a new registry and registers all the built-in
        node processors for the standard opcodes used in the replay system.
        
        Returns:
            NodeProcessorRegistry: A fully configured registry with all standard processors
        """
        registry = cls()
        registry.register(Opcode.TEMPLATE, TemplateNodeProcessor())
        registry.register(Opcode.DOCS, DocNodeProcessor())
        registry.register(Opcode.PROMPT, PromptNodeProcessor())
        registry.register(Opcode.RUN, RunNodeProcessor())        
        registry.register(Opcode.CONDITIONAL, ConditionalNodeProcessor())
        registry.register(Opcode.FIX, FixNodeProcessor())
        registry.register(Opcode.EXIT, ExitNodeProcessor())
        return registry