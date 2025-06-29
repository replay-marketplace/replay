import os
import json
import networkx as nx
import logging
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Any, Dict
from core.dir_preprocessing import setup_project_directories, post_replay_dir_cleanup
from core.prompt_preprocess2.processor3 import prompt_preprocess3
from core.prompt_preprocess2.ir.ir import EpicIR, Opcode
from core.backend import NodeProcessorRegistry

logger = logging.getLogger(__name__)

def create_client(use_mock: bool = False):
    """
    Create and return an appropriate client based on configuration.
    
    Args:
        use_mock: If True, use MockAnthropicClient. If False, use real Anthropic client.
    
    Returns:
        Client instance (MockAnthropicClient or anthropic.Anthropic)
    """
    if use_mock:
        from core.backend.mock_anthropic import MockAnthropicClient
        return MockAnthropicClient()
    else:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")
        import anthropic
        return anthropic.Anthropic(api_key=api_key)

@dataclass
class InputConfig:
    input_prompt_file: Optional[str] = None
    project_name: Optional[str] = None
    output_dir: str = "replay_output"

@dataclass
class InitState:
    epic_graph: Optional[Dict] = None
    dfs_nodes: List[Any] = field(default_factory=list)
    setup_done: bool = False
    preprocess_done: bool = False

@dataclass
class ExecutionState:
    current_node_idx: int = 0
    finished: bool = False

@dataclass
class ReplayState:
    input_config: InputConfig = field(default_factory=InputConfig)
    init: InitState = field(default_factory=InitState)
    execution: ExecutionState = field(default_factory=ExecutionState)

    def to_dict(self) -> dict:
        return {
            "input_config": asdict(self.input_config),
            "init": asdict(self.init),
            "execution": asdict(self.execution),
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            input_config=InputConfig(**d.get("input_config", {})),
            init=InitState(**d.get("init", {})),
            execution=ExecutionState(**d.get("execution", {})),
        )

class Replay:
    def __init__(
        self,
        input_config: Optional[InputConfig] = None,
        state: Optional[ReplayState] = None,
        client=None,
        session_folder: str = None,
        use_mock: bool = False
    ):
        if state is not None:
            self.state = state
        elif input_config is not None:
            self.state = ReplayState(input_config=input_config)
        else:
            raise ValueError("Must provide either input_config or state")
        self.client = client
        self.use_mock = use_mock
        self.code_dir = None
        self.replay_dir = None
        self.project_dir = None
        self.latest_dir = None
        self.epic_dir = session_folder
        self.system_instructions = None
        self.epic = None
        self.dfs_nodes = []  # Initialize dfs_nodes to prevent AttributeError
        self.node_processor_registry = NodeProcessorRegistry.create_registry()
        
        # If we have a state with dfs_nodes, restore them
        if state is not None and state.init.dfs_nodes:
            self.dfs_nodes = state.init.dfs_nodes

    def setup(self, clear_terminal: bool = False):
        if self.state.init.setup_done:
            return
        if clear_terminal:
            os.system('cls' if os.name == 'nt' else 'clear')
        self._init_client()
        self._setup_directories()
        self._load_system_instructions()
        self.state.init.setup_done = True

    def run_step(self):
        if not self.state.init.preprocess_done:
            self.preprocess()
        if not self.has_steps():
            return
        node = self.dfs_nodes[self.state.execution.current_node_idx]
        opcode = self.epic.graph.nodes[node]['opcode']
        processor = self.node_processor_registry.get(opcode)
        if processor is None:
            raise ValueError(f"No processor registered for opcode: {opcode}")
        logger.debug(f"\n\n--- RUNTIME: start {opcode.name.lower()}: ---- ")
        processor.process(self, node)
        logger.debug(f"--- {opcode.name.lower()}: END ----")
        self.state.execution.current_node_idx += 1
        if self.state.execution.current_node_idx >= len(self.dfs_nodes):
            self.state.execution.finished = True
            post_replay_dir_cleanup(self.project_dir, self.latest_dir, self.epic_dir)

    def run_all(self):
        self.setup()
        self.preprocess()
        while self.has_steps():
            self.run_step()

    def save_state(self):
        state_path = os.path.join(self.replay_dir, "replay_state.json")
        with open(state_path, 'w') as f:
            json.dump(self.state.to_dict(), f, indent=2)

    def _copy_reference_content(self):
        """
        Copy all /TEMPLATE and /DOCS content referenced in the graph to the session's template/ and docs/ folders.
        Also copy template content to the code directory as initial code structure.
        """
        logger.info("Copying reference content to session folder...")
        prompt_dir = os.path.dirname(os.path.abspath(self.state.input_config.input_prompt_file))
        session_dir = self.epic_dir
        template_dst = os.path.join(session_dir, "template")
        docs_dst = os.path.join(session_dir, "docs")
        code_dst = self.code_dir
        import shutil

        # Copy /TEMPLATE directory
        for node in self.epic.graph.nodes():
            node_data = self.epic.graph.nodes[node]
            if node_data.get('opcode') == Opcode.TEMPLATE:
                path = node_data.get('contents', {}).get('path')
                if path:
                    src_path = os.path.join(prompt_dir, path) if not os.path.isabs(path) else path
                    if os.path.exists(src_path):
                        if os.path.isdir(src_path):
                            # Copy to template directory
                            if os.path.exists(template_dst):
                                shutil.rmtree(template_dst)
                            shutil.copytree(src_path, template_dst)
                            logger.info(f"Copied TEMPLATE dir: {src_path} -> {template_dst}")
                            
                            # Copy to code directory as initial structure
                            if os.path.exists(code_dst):
                                shutil.rmtree(code_dst)
                            shutil.copytree(src_path, code_dst)
                            logger.info(f"Copied TEMPLATE dir to code: {src_path} -> {code_dst}")
                        elif os.path.isfile(src_path):
                            # Copy to template directory
                            os.makedirs(template_dst, exist_ok=True)
                            shutil.copy2(src_path, os.path.join(template_dst, os.path.basename(src_path)))
                            logger.info(f"Copied TEMPLATE file: {src_path} -> {template_dst}")
                            
                            # Copy to code directory
                            os.makedirs(code_dst, exist_ok=True)
                            shutil.copy2(src_path, os.path.join(code_dst, os.path.basename(src_path)))
                            logger.info(f"Copied TEMPLATE file to code: {src_path} -> {code_dst}")
                        else:
                            logger.warning(f"TEMPLATE path is not a file or directory: {src_path}")
                    else:
                        logger.warning(f"TEMPLATE path does not exist: {src_path}")

        # Copy /DOCS directory
        for node in self.epic.graph.nodes():
            node_data = self.epic.graph.nodes[node]
            if node_data.get('opcode') == Opcode.DOCS:
                path = node_data.get('contents', {}).get('path')
                if path:
                    src_path = os.path.join(prompt_dir, path) if not os.path.isabs(path) else path
                    if os.path.exists(src_path):
                        if os.path.isdir(src_path):
                            if os.path.exists(docs_dst):
                                shutil.rmtree(docs_dst)
                            shutil.copytree(src_path, docs_dst)
                            logger.info(f"Copied DOCS dir: {src_path} -> {docs_dst}")
                        elif os.path.isfile(src_path):
                            os.makedirs(docs_dst, exist_ok=True)
                            shutil.copy2(src_path, os.path.join(docs_dst, os.path.basename(src_path)))
                            logger.info(f"Copied DOCS file: {src_path} -> {docs_dst}")
                        else:
                            logger.warning(f"DOCS path is not a file or directory: {src_path}")
                    else:
                        logger.warning(f"DOCS path does not exist: {src_path}")

        logger.info("Reference content copy complete.")

    def preprocess(self):
        if not self.state.init.setup_done:
            self.setup()
        self.epic = prompt_preprocess3(self.state.input_config.input_prompt_file, self.replay_dir)
        self.dfs_nodes = list(nx.dfs_preorder_nodes(self.epic.graph, self.epic.first_node))
        self.state.init.dfs_nodes = self.dfs_nodes  # Save dfs_nodes to state
        self.state.execution.current_node_idx = 0
        self.state.init.preprocess_done = True
        self.state.execution.finished = False
        # Print the parsed graph for debugging
        print("\n=== Parsed Graph Nodes ===")
        for node in self.epic.graph.nodes(data=True):
            print(node)
        print("=== End Parsed Graph Nodes ===\n")
        # Copy all reference content to the session's template/ and docs/ folders
        self._copy_reference_content()

    def has_steps(self):
        return self.state.execution.current_node_idx < len(self.dfs_nodes) and not self.state.execution.finished

    def _init_client(self):
        if self.client is None:
            self.client = create_client(use_mock=self.use_mock)

    def _load_system_instructions(self):
        try:
            instructions_path = os.path.join(self.replay_dir, "client_instructions_with_json.txt")
            with open(instructions_path, "r") as f:
                self.system_instructions = f.read()
        except FileNotFoundError:
            raise RuntimeError("System instructions file not found in session replay folder.")

    def _setup_directories(self):
        if self.epic_dir is None:
            (self.code_dir, self.replay_dir, self.project_dir,
             self.latest_dir, self.epic_dir) = setup_project_directories(
                self.state.input_config.output_dir, self.state.input_config.project_name)
        else:
            self.code_dir = os.path.join(self.epic_dir, "code")
            self.replay_dir = os.path.join(self.epic_dir, "replay")
            self.project_dir = os.path.dirname(self.epic_dir)
            self.latest_dir = os.path.join(self.project_dir, "latest")
        # Copy system instructions to the session's replay folder
        src_instructions = "core/backend/client_instructions_with_json.txt"
        dst_instructions = os.path.join(self.replay_dir, "client_instructions_with_json.txt")
        if os.path.exists(src_instructions):
            import shutil
            shutil.copy(src_instructions, dst_instructions)
        else:
            raise RuntimeError("System instructions file not found in core/backend/")

    def _restore_epic_from_state(self):
        """Restore EpicIR from state if available"""
        if self.state.init.epic_graph is not None:
            self.epic = EpicIR.from_dict(self.state.init.epic_graph)
            return True
        return False

    def load_pass_graph(self, pass_name: str):
        """
        Load a specific pass graph from the saved files for debugging.
        
        Args:
            pass_name: Name of the pass file (e.g., 'pass1_build_graph', 'pass2_insert_exit', etc.)
        """
        pass_file = os.path.join(self.replay_dir, f"{pass_name}.json")
        if not os.path.exists(pass_file):
            raise FileNotFoundError(f"Pass file not found: {pass_file}")
        
        with open(pass_file, 'r') as f:
            graph_data = json.load(f)
        
        self.epic = EpicIR.from_dict(graph_data)
        self.dfs_nodes = list(nx.dfs_preorder_nodes(self.epic.graph, self.epic.first_node))
        self.state.init.dfs_nodes = self.dfs_nodes
        self.state.init.epic_graph = graph_data
        self.state.init.preprocess_done = True
        self.state.execution.current_node_idx = 0
        self.state.execution.finished = False
        
        logger.info(f"Loaded pass graph: {pass_name}")
        return self.epic