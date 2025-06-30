import os
import json
import networkx as nx
import logging
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Any, Dict
from enum import Enum
from core.dir_preprocessing import setup_project_directories, post_replay_dir_cleanup
from core.prompt_preprocess2.processor3 import prompt_preprocess3
from core.prompt_preprocess2.ir.ir import EpicIR, Opcode
from core.backend import NodeProcessorRegistry

logger = logging.getLogger(__name__)

class ReplayStatus(Enum):
    UNINITIALIZED = "uninitialized"
    INITIALIZED = "initialized"
    COMPILING_PROGRAM = "compiling_program"
    LOADED_PROGRAM = "loaded_program"
    RUNNING_PROGRAM = "running_program"
    FINISHED_RUNNING_PROGRAM = "finished_running_program"

@dataclass
class InputConfig:
    input_prompt_file: Optional[str] = None
    project_name: Optional[str] = None
    output_dir: str = "replay_output"

@dataclass
class ExecutionState:
    """Contains the runtime execution state (like CPU state with loaded program)"""
    current_node_idx: int = 0
    epic: Optional[EpicIR] = None  # The loaded program
    dfs_nodes: List[Any] = field(default_factory=list)  # Execution order
    
    def to_dict(self) -> dict:
        return {
            "current_node_idx": self.current_node_idx,
            "epic": self.epic.to_dict() if self.epic else None,
            "dfs_nodes": self.dfs_nodes,
        }
    
    @classmethod
    def from_dict(cls, d: dict):
        epic_data = d.get("epic")
        epic = EpicIR.from_dict(epic_data) if epic_data else None
        return cls(
            current_node_idx=d.get("current_node_idx", 0),
            epic=epic,
            dfs_nodes=d.get("dfs_nodes", []),
        )

@dataclass
class ReplayState:
    input_config: InputConfig = field(default_factory=InputConfig)
    execution: ExecutionState = field(default_factory=ExecutionState)
    status: ReplayStatus = ReplayStatus.UNINITIALIZED
    version: Optional[str] = None  # Add version info

    def to_dict(self) -> dict:
        return {
            "input_config": asdict(self.input_config),
            "execution": self.execution.to_dict(),
            "status": self.status.value,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            input_config=InputConfig(**d.get("input_config", {})),
            execution=ExecutionState.from_dict(d.get("execution", {})),
            status=ReplayStatus(d.get("status", ReplayStatus.UNINITIALIZED.value)),
            version=d.get("version"),
        )
    
    def save(self, file_path: str):
        """Save the state to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

class Replay:
    def __init__(
        self,
        state: ReplayState,
        client=None,
        use_mock: bool = False
    ):
        self.state = state
        self.client = client
        self.use_mock = use_mock
        self.project_dir = os.path.join(self.state.input_config.output_dir, self.state.input_config.project_name)
        self.version_dir = None
        self.replay_dir = None
        self.code_dir = None
        self.docs_dir = None
        self.template_dir = None
        self.latest_dir = os.path.join(self.project_dir, "latest")
        self.system_instructions = None
        self.node_processor_registry = NodeProcessorRegistry.create_registry()
        self._setup_directories()
        if self.state.status != ReplayStatus.UNINITIALIZED:
            self._init_client()
            self._load_system_instructions()

    @classmethod
    def from_recipe(
        cls,
        input_config: InputConfig,
        client=None,
        use_mock: bool = False
    ) -> 'Replay':
        """Create a new Replay instance from input configuration (recipe), always creating a new version."""
        # Find next version number
        project_dir = os.path.join(input_config.output_dir, input_config.project_name)
        os.makedirs(project_dir, exist_ok=True)
        version = cls._get_next_version(project_dir)
        state = ReplayState(input_config=input_config, version=version)
        return cls(state, client=client, use_mock=use_mock)

    @classmethod
    def load_checkpoint(
        cls,
        project_name: str,
        output_dir: str = "replay_output",
        version: str = "latest",
        client=None,
        use_mock: bool = False
    ) -> 'Replay':
        """Load a Replay instance from a project directory checkpoint for a specific version (or latest)."""
        project_dir = os.path.join(output_dir, project_name)
        if version == "latest":
            version_dir = os.path.realpath(os.path.join(project_dir, "latest"))
        else:
            version_dir = os.path.realpath(os.path.join(project_dir, str(version)))
        replay_dir = os.path.join(version_dir, "replay")
        state_path = os.path.join(replay_dir, "replay_state.json")
        if not os.path.exists(state_path):
            raise FileNotFoundError(f"State file not found: {state_path}")
        with open(state_path, 'r') as f:
            loaded_state = ReplayState.from_dict(json.load(f))
            logger.info(f"State loaded from {state_path}")
            return cls(loaded_state, client=client, use_mock=use_mock)

    @staticmethod
    def _get_next_version(project_dir: str) -> str:
        versions = [int(d) for d in os.listdir(project_dir) if d.isdigit()]
        next_version = str(max(versions) + 1 if versions else 1)
        return next_version

    @property
    def status(self) -> ReplayStatus:
        """Get the current replay status."""
        return self.state.status

    @status.setter
    def status(self, new_status: ReplayStatus):
        """Set the replay status with logging."""
        old_status = self.state.status
        if old_status != new_status:
            logger.info(f"Replay status: {old_status.value} → {new_status.value}")
            self.state.status = new_status

    def setup(self, clear_terminal: bool = False):
        if self.state.status != ReplayStatus.UNINITIALIZED:
            return
        if clear_terminal:
            os.system('cls' if os.name == 'nt' else 'clear')
        self._init_client()
        self._setup_directories()
        self._load_system_instructions()
        self.status = ReplayStatus.INITIALIZED

    def run_step(self):
        if self.state.status == ReplayStatus.UNINITIALIZED:
            self.setup()
        if self.state.status == ReplayStatus.COMPILING_PROGRAM:
            self.compile()
        if self.state.status == ReplayStatus.LOADED_PROGRAM:
            self.status = ReplayStatus.RUNNING_PROGRAM
        if not self.has_steps():
            return
            
        node = self.state.execution.dfs_nodes[self.state.execution.current_node_idx]
        opcode = self.state.execution.epic.graph.nodes[node]['opcode']
        processor = self.node_processor_registry.get(opcode)
        if processor is None:
            raise ValueError(f"No processor registered for opcode: {opcode}")
        logger.debug(f"\n\n--- RUNTIME: start {opcode.name.lower()}: ---- ")
        processor.process(self, node)
        logger.debug(f"--- {opcode.name.lower()}: END ----")
        self.state.execution.current_node_idx += 1
        if self.state.execution.current_node_idx >= len(self.state.execution.dfs_nodes):
            self.status = ReplayStatus.FINISHED_RUNNING_PROGRAM
            post_replay_dir_cleanup(self.project_dir, self.latest_dir, self.version_dir)

    def run_all(self):
        self.setup()
        self.compile()
        while self.has_steps():
            self.run_step()

    def get_program(self) -> ExecutionState:
        """Return the program (graph) state."""
        return self.state.execution

    def get_execution_state(self) -> ExecutionState:
        """Return the execution state."""
        return self.state.execution

    def get_status(self) -> ReplayStatus:
        """Return the current replay status."""
        return self.status

    def get_state(self) -> ReplayState:
        """Return the complete state (program + execution + config)."""
        return self.state

    def save_state(self):
        state_path = os.path.join(self.replay_dir, "replay_state.json")
        self.state.save(state_path)
        logger.info(f"State saved to {state_path}")

    def _copy_reference_content(self):
        """
        Copy all /TEMPLATE and /DOCS content referenced in the graph to the version's template/ and docs/ folders.
        Also copy template content to the code directory as initial code structure.
        """
        logger.info("Copying reference content to version folder...")
        prompt_dir = os.path.dirname(os.path.abspath(self.state.input_config.input_prompt_file))
        version_dir = self.version_dir
        template_dst = self.template_dir
        docs_dst = self.docs_dir
        code_dst = self.code_dir
        import shutil

        # Copy /TEMPLATE directory
        for node in self.state.execution.epic.graph.nodes():
            node_data = self.state.execution.epic.graph.nodes[node]
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
        for node in self.state.execution.epic.graph.nodes():
            node_data = self.state.execution.epic.graph.nodes[node]
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

    def compile(self):        
        if self.state.status != ReplayStatus.INITIALIZED:
            self.setup()
        self.status = ReplayStatus.COMPILING_PROGRAM
        self.state.execution.epic = prompt_preprocess3(self.state.input_config.input_prompt_file, self.replay_dir)
        self.state.execution.dfs_nodes = list(nx.dfs_preorder_nodes(self.state.execution.epic.graph, self.state.execution.epic.first_node))
        self.state.execution.current_node_idx = 0
        # Print the parsed graph for debugging
        print("\n=== Parsed Graph Nodes ===")
        for node in self.state.execution.epic.graph.nodes(data=True):
            print(node)
        print("=== End Parsed Graph Nodes ===\n")
        # Copy all reference content to the session's template/ and docs/ folders
        self._copy_reference_content()
        self.status = ReplayStatus.LOADED_PROGRAM

    def has_steps(self):
        return (self.state.execution.current_node_idx < len(self.state.execution.dfs_nodes) and 
                self.state.status != ReplayStatus.FINISHED_RUNNING_PROGRAM)

    def _init_client(self):
        """
        Setup the client based on configuration (use_mock or ANTHROPIC_API_KEY)
        """
        if self.client is not None:
            return
            
        if self.use_mock:
            from core.backend.mock_anthropic import MockAnthropicClient
            self.client = MockAnthropicClient()
        else:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)            

    def _load_system_instructions(self):
        try:
            instructions_path = os.path.join(self.replay_dir, "client_instructions_with_json.txt")
            with open(instructions_path, "r") as f:
                self.system_instructions = f.read()
        except FileNotFoundError:
            raise RuntimeError("System instructions file not found in session replay folder.")

    def _setup_directories(self):
        # Set up all relevant directories for this version
        version = self.state.version or "1"
        self.version_dir = os.path.join(self.project_dir, version)
        self.replay_dir = os.path.join(self.version_dir, "replay")
        self.code_dir = os.path.join(self.version_dir, "code")
        self.docs_dir = os.path.join(self.version_dir, "docs")
        self.template_dir = os.path.join(self.version_dir, "template")
        os.makedirs(self.replay_dir, exist_ok=True)
        os.makedirs(self.code_dir, exist_ok=True)
        os.makedirs(self.docs_dir, exist_ok=True)
        os.makedirs(self.template_dir, exist_ok=True)
        # Copy system instructions (before touching symlink)
        src_instructions = "core/backend/client_instructions_with_json.txt"
        dst_instructions = os.path.join(self.replay_dir, "client_instructions_with_json.txt")
        if os.path.exists(src_instructions):
            import shutil
            shutil.copy(src_instructions, dst_instructions)
        else:
            raise RuntimeError("System instructions file not found in core/backend/")
        # Only update latest symlink if this is actually the latest version
        # Check if this version is actually the latest
        versions = [int(d) for d in os.listdir(self.project_dir) if d.isdigit()]
        if versions and version.isdigit() and int(version) == max(versions):
            if os.path.islink(self.latest_dir) or os.path.isfile(self.latest_dir):
                os.unlink(self.latest_dir)
            elif os.path.isdir(self.latest_dir):
                import shutil
                shutil.rmtree(self.latest_dir)
            os.symlink(self.version_dir, self.latest_dir)