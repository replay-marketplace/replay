from .template_node_processor import TemplateNodeProcessor
from .prompt_node_processor import PromptNodeProcessor
from .run_node_processor import RunNodeProcessor
from .exit_node_processor import ExitNodeProcessor
from .doc_node_processor import DocNodeProcessor
from core.prompt_preprocess2.ir.ir import Opcode

class NodeProcessorRegistry:
    def __init__(self):
        self._registry = {}
    def register(self, opcode, processor):
        self._registry[opcode] = processor
    def get(self, opcode):
        return self._registry.get(opcode)

    @classmethod
    def create_registry(cls):
        registry = cls()
        registry.register(Opcode.TEMPLATE, TemplateNodeProcessor())
        registry.register(Opcode.PROMPT, PromptNodeProcessor())
        registry.register(Opcode.RUN, RunNodeProcessor())
        registry.register(Opcode.EXIT, ExitNodeProcessor())
        registry.register(Opcode.DOCS, DocNodeProcessor())
        return registry