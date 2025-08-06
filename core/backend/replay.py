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
from core.backend.processors import NodeProcessorRegistry
from core.backend.git_manager import GitManager, MockGitManager
from datetime import datetime

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
    current_node_id: Optional[str] = None
    control_flow_graph_queue: List[Optional[str]] = field(default_factory=list)
    epic: Optional[EpicIR] = None  # The loaded program
    memory: List[str] = field(default_factory=list)
    step_count: int = 0  # Track number of steps executed
    
    def to_dict(self) -> dict:
        return {
            "current_node_id": self.current_node_id,
            "control_flow_graph_queue": self.control_flow_graph_queue,
            "epic": self.epic.to_dict() if self.epic else None,
            "memory": self.memory,
            "step_count": self.step_count,
        }
    
    @classmethod
    def from_dict(cls, d: dict):        
        epic_data = d.get("epic")
        epic = EpicIR.from_dict(epic_data) if epic_data else None
        current_node_id = d.get("current_node_id", None)
        control_flow_graph_queue = d.get("control_flow_graph_queue", [])

        return cls(
            current_node_id=current_node_id,
            control_flow_graph_queue=control_flow_graph_queue,
            epic=epic,
            memory=d.get("memory", []),
            step_count=d.get("step_count", 0),
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
        use_mock: bool = False,
        llm_backend: str = "claude_code",
        disable_git: bool = False
    ):
        self.state = state
        self.client = client
        self.use_mock = use_mock
        self.llm_backend_name = llm_backend
        self.disable_git = disable_git
        self.llm_backend = None  # Will be initialized in _init_llm_backend
        self.project_dir = os.path.join(self.state.input_config.output_dir, self.state.input_config.project_name)
        self.version_dir = None
        self.replay_dir = None
        self.code_dir = None
        self.docs_dir = None
        self.template_dir = None
        self.latest_dir = os.path.join(self.project_dir, "latest")
        self.system_instructions = None
        self.node_processor_registry = NodeProcessorRegistry.create_registry()
        self.git_manager = MockGitManager(self.project_dir)  # Will be overridden in _setup_directories if git is enabled

        self._setup_directories()
        self._init_client()
        self._init_llm_backend()
        self._load_system_instructions()              

        if self.state.status not in (ReplayStatus.LOADED_PROGRAM, ReplayStatus.RUNNING_PROGRAM):
            self.status = ReplayStatus.INITIALIZED


    @classmethod
    def from_recipe(
        cls,
        input_config: InputConfig,
        client=None,
        use_mock: bool = False,
        llm_backend: str = "claude_code",
        disable_git: bool = False
    ) -> 'Replay':
        """Create a new Replay instance from input configuration (recipe), always creating a new version."""
        # Find next version number
        logger.info(f"Creating new Replay instance from input configuration: {input_config}")
        project_dir = os.path.join(input_config.output_dir, input_config.project_name)
        os.makedirs(project_dir, exist_ok=True)
        version = cls._get_next_version(project_dir)
        state = ReplayState(input_config=input_config, version=version)
        return cls(state, client=client, use_mock=use_mock, llm_backend=llm_backend, disable_git=disable_git)

    @classmethod
    def load_checkpoint(
        cls,
        project_name: str,
        output_dir: str = "replay_output",
        version: str = "latest",
        client=None,
        use_mock: bool = False,
        llm_backend: str = "claude_code",
        disable_git: bool = False
    ) -> 'Replay':
        """Load a Replay instance from a project directory checkpoint for a specific version (or latest)."""
        logger.info(f"Creating new Replay instance from checkpoint: {output_dir} / {project_name} / {version}")
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
            
            return cls(loaded_state, client=client, use_mock=use_mock, llm_backend=llm_backend, disable_git=disable_git)

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

    def run_step(self):
        if self.state.status == ReplayStatus.FINISHED_RUNNING_PROGRAM:
            return
        
        if self.state.status == ReplayStatus.INITIALIZED:
            self.compile()
        if self.state.status == ReplayStatus.LOADED_PROGRAM:
            self.status = ReplayStatus.RUNNING_PROGRAM
        if self.state.status == ReplayStatus.RUNNING_PROGRAM and not self.has_steps():
            return
        
        assert self.state.execution.current_node_id is not None, "Current node can't be None here"
        
        current_node_id = self.state.execution.current_node_id
        if current_node_id is None:
            logger.warning("No steps to run")
            return
        current_node = self.state.execution.epic.graph.nodes[current_node_id]
        if current_node is None:
            logger.warning(f"Current node not found: {current_node_id}")
            return
        
        opcode = current_node['opcode']
        processor = self.node_processor_registry.get(opcode)
        if processor is None:
            raise ValueError(f"No processor registered for opcode: {opcode}")
        started = datetime.now()
        logger.info(f"\n\n--- RUNTIME: start {opcode.name.lower()}: ---- ")
        processor.process(self, current_node)
        ended = datetime.now()
        duration = ended - started

        logger.info(f"--- {opcode.name.lower()}: END | Took: {duration} ----")

        # Increment step counter
        self.state.execution.step_count += 1
        
        # Commit changes after step execution
        self.git_manager.commit_step(current_node, opcode, self.state.execution.step_count)

        # Check if this is a control flow node that determines its own next node
        if opcode == Opcode.CONDITIONAL:
            # This is a hack to which I see 3 options:
            # - this (I do prefer this for now)
            # - let each node choose next node
            # - switch to two phases
            # For control flow nodes, let the processor set the next node
            # The processor should have updated current_node_id appropriately
            pass
        else:
            # Determine next node using CFG traversal
            from core.prompt_preprocess2.ir.control_flow import cfg_traversal_step        
            cfg_queue, next_node_id = cfg_traversal_step(self.state.execution.epic, self.state.execution.control_flow_graph_queue)
            self.state.execution.control_flow_graph_queue = cfg_queue
            self.state.execution.current_node_id = next_node_id

        if len(self.state.execution.control_flow_graph_queue) and self.state.execution.current_node_id is None:            
            self.status = ReplayStatus.FINISHED_RUNNING_PROGRAM
            post_replay_dir_cleanup(self.project_dir, self.latest_dir, self.version_dir)

    def run_all(self):
        if self.state.status == ReplayStatus.INITIALIZED:
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
        Copy all /TEMPLATE and /DOCS content referenced in the graph to the replay directory only.
        Templates and docs are read-only resources, so we don't need them in version_dir.
        """
        logger.info("Copying reference content to replay directory...")
        
        # Always use the replay directory as the base for path resolution
        # This ensures all paths are relative to prompt.txt in the replay directory
        base_dir = self.replay_dir
        import shutil

        def resolve_source_path(path):
            """Resolve source path based on whether this is a new run or checkpoint load."""
            prompt_file_path = os.path.abspath(self.state.input_config.input_prompt_file)
            replay_dir_path = os.path.abspath(base_dir)
            
            logger.debug(f"resolve_source_path: path={path}")
            logger.debug(f"resolve_source_path: prompt_file_path={prompt_file_path}")
            logger.debug(f"resolve_source_path: replay_dir_path={replay_dir_path}")
            
            # Check if this is a checkpoint load by seeing if the prompt file is in the replay directory
            if os.path.dirname(prompt_file_path) == replay_dir_path:
                # This is a checkpoint load - resolve from replay directory
                resolved = os.path.join(base_dir, path) if not os.path.isabs(path) else path
                logger.debug(f"resolve_source_path: checkpoint load, resolved={resolved}")
                return resolved
            else:
                # This is a new run - try multiple resolution strategies
                if os.path.isabs(path):
                    # Strategy 1: Absolute path
                    logger.debug(f"resolve_source_path: absolute path, resolved={path}")
                    return path
                
                prompt_dir = os.path.dirname(prompt_file_path)
                prompt_parent_dir = os.path.dirname(prompt_dir)
                
                # Strategy 2: Relative to prompt file directory
                candidate1 = os.path.join(prompt_dir, path)
                if os.path.exists(candidate1):
                    logger.debug(f"resolve_source_path: found relative to prompt dir, resolved={candidate1}")
                    return candidate1
                
                # Strategy 3: Relative to prompt dir's parent
                candidate2 = os.path.join(prompt_parent_dir, path)
                if os.path.exists(candidate2):
                    logger.debug(f"resolve_source_path: found relative to prompt parent dir, resolved={candidate2}")
                    return candidate2
                
                raise ValueError(f"Path does not exist: {path}")                

        def copy_to_replay_only(src_path, replay_path):
            """Copy file/directory to replay directory only (read-only resources)."""
            if not os.path.exists(src_path):
                logger.warning(f"Path does not exist: {src_path}")
                return False
            
            # Copy to replay directory only
            if os.path.isdir(src_path):
                if os.path.exists(replay_path):
                    shutil.rmtree(replay_path)
                shutil.copytree(src_path, replay_path)
                logger.info(f"Copied directory to replay: {src_path} -> {replay_path}")
            elif os.path.isfile(src_path):
                os.makedirs(base_dir, exist_ok=True)
                shutil.copy2(src_path, replay_path)
                logger.info(f"Copied file to replay: {src_path} -> {replay_path}")
            else:
                logger.warning(f"Path is not a file or directory: {src_path}")
                return False
            
            return True

        def copy_template_to_code(src_path, replay_path):
            """Copy template to replay directory and also to code directory as initial structure."""
            if not os.path.exists(src_path):
                logger.warning(f"Path does not exist: {src_path}")
                return False
            
            # Copy to replay directory first
            if os.path.isdir(src_path):
                if os.path.exists(replay_path):
                    shutil.rmtree(replay_path)
                shutil.copytree(src_path, replay_path)
                logger.info(f"Copied template directory to replay: {src_path} -> {replay_path}")
                
                # Also copy to code directory as initial structure
                if os.path.exists(self.code_dir):
                    shutil.rmtree(self.code_dir)
                shutil.copytree(replay_path, self.code_dir)
                logger.info(f"Copied template directory to code: {replay_path} -> {self.code_dir}")
            elif os.path.isfile(src_path):
                os.makedirs(base_dir, exist_ok=True)
                shutil.copy2(src_path, replay_path)
                logger.info(f"Copied template file to replay: {src_path} -> {replay_path}")
                
                # Also copy to code directory
                os.makedirs(self.code_dir, exist_ok=True)
                shutil.copy2(replay_path, os.path.join(self.code_dir, os.path.basename(src_path)))
                logger.info(f"Copied template file to code: {replay_path} -> {self.code_dir}")
            else:
                logger.warning(f"Path is not a file or directory: {src_path}")
                return False
            
            return True

        # Copy all referenced resources to replay directory only
        for node in self.state.execution.epic.graph.nodes():
            node_data = self.state.execution.epic.graph.nodes[node]
            opcode = node_data.get('opcode')
            
            if opcode == Opcode.TEMPLATE:
                path = node_data.get('contents', {}).get('path')
                if path:
                    src_path = resolve_source_path(path)
                    replay_path = os.path.join(self.template_dir, os.path.basename(path))
                    copy_template_to_code(src_path, replay_path)
            elif opcode == Opcode.DOCS:
                path = node_data.get('contents', {}).get('path')
                if path:
                    src_path = resolve_source_path(path)
                    replay_path = os.path.join(self.docs_dir, os.path.basename(path))
                    copy_to_replay_only(src_path, replay_path)

        logger.info("Reference content copy complete.")

    def compile(self):
        self.status = ReplayStatus.COMPILING_PROGRAM
        self.state.execution.epic = prompt_preprocess3(self.state.input_config.input_prompt_file, self.replay_dir, save_passes=False)        
        self.state.execution.control_flow_graph_queue = [self.state.execution.epic.first_node]
        self.state.execution.current_node_id = self.state.execution.epic.first_node
        
        # Print the parsed graph for debugging
        print("\n=== Parsed Graph Nodes ===")
        for node in self.state.execution.epic.graph.nodes(data=True):
            print(node)
        print("=== End Parsed Graph Nodes ===\n")
        # Copy all reference content to the session's template/ and docs/ folders
        self._copy_reference_content()
        
        # Initial commit after compilation
        self.git_manager.commit_initial()
        
        self.status = ReplayStatus.LOADED_PROGRAM

    def has_steps(self):
        return (self.state.execution.current_node_id is not None)

    def _init_client(self):
        """
        Setup the client based on configuration (use_mock, backend type)
        """
        if self.client is not None:
            return
            
        if self.use_mock:
            from core.backend.client.mock_anthropic import MockAnthropicClient
            base_client = MockAnthropicClient()
            # Wrap the mock client to save all requests and responses
            from core.backend.client.client_wrapper import ClientWrapper
            self.client = ClientWrapper(base_client, self.version_dir)
        elif self.llm_backend_name == "claude_code":
            # Use Claude Code SDK with async query wrapped for synchronous interface
            logger.info("Using Claude Code SDK with async query wrapper")
            from core.backend.client.claude_code_client_wrapper import ClaudeCodeClientWrapper
            self.client = ClaudeCodeClientWrapper(self.version_dir)
        elif self.llm_backend_name == "anthropic_api":
            # Use standard Anthropic API client
            logger.info("Using standard Anthropic API client")
            try:
                import anthropic
                # Create standard Anthropic client
                self.client = anthropic.Anthropic()
                logger.info("Initialized standard Anthropic client")
            except ImportError as e:
                raise RuntimeError("anthropic package is required for anthropic_api backend. Install with: pip install anthropic") from e
            except Exception as e:
                raise RuntimeError(f"Failed to initialize Anthropic client: {e}") from e
        else:
            raise ValueError(f"Unknown LLM backend: {self.llm_backend_name}")

    def _init_llm_backend(self):
        """
        Initialize the LLM backend based on configuration.
        """
        if self.llm_backend_name == "claude_code":
            from .claude_code_backend import ClaudeCodeBackend
            self.llm_backend = ClaudeCodeBackend(client=self.client)
            logger.info("Initialized Claude Code backend")
        elif self.llm_backend_name == "anthropic_api":
            from .anthropic_api_backend import AnthropicAPIBackend
            # For anthropic API, we need to use a standard model name
            self.llm_backend = AnthropicAPIBackend(model_name="claude-3-7-sonnet-20250219", client=self.client)
            logger.info("Initialized Anthropic API backend")
        else:
            raise ValueError(f"Unknown LLM backend: {self.llm_backend_name}")

    def _load_system_instructions(self):
        # System instructions are now handled by the LLM backends
        # This method is kept for backward compatibility but doesn't load anything
        # The backends will load their appropriate instruction files when needed
        self.system_instructions = None

    def _copy_system_instructions(self):
        import pkg_resources
        # Copy both backend-specific instruction files
        src_instructions = ["client_instructions_with_json_claude.txt",
                            "client_instructions_with_json_anthropic.txt",
                            "client_instructions_indentify_issue.txt"]
        dst_instructions = os.path.join(self.replay_dir)        
        for src_instruction in src_instructions:
            # Use pkg_resources to find the file within the installed package
            resource_path = f"core/backend/system_prompts/{src_instruction}"
            dst_instruction = os.path.join(self.replay_dir, src_instruction)
            
            try:
                # Read the resource content
                content = pkg_resources.resource_string("core", f"backend/system_prompts/{src_instruction}")
                # Write to destination
                with open(dst_instruction, 'wb') as f:
                    f.write(content)
            except Exception as e:
                raise RuntimeError(f"System instructions file not found: {resource_path}. Error: {e}")

    def _setup_directories(self):
        # Set up all relevant directories for this version
        version = self.state.version or "1"
        self.version_dir = os.path.join(self.project_dir, version)
        self.replay_dir = os.path.join(self.version_dir, "replay")
        self.code_dir = os.path.join(self.version_dir, "code")
        self.docs_dir = os.path.join(self.replay_dir, "docs")
        self.run_logs_dir = os.path.join(self.replay_dir, "run_logs")
        self.template_dir = os.path.join(self.replay_dir, "template")
        os.makedirs(self.replay_dir, exist_ok=True)
        os.makedirs(self.code_dir, exist_ok=True)
        os.makedirs(self.docs_dir, exist_ok=True)
        os.makedirs(self.run_logs_dir, exist_ok=True)
        os.makedirs(self.template_dir, exist_ok=True)
        
        self._copy_system_instructions()
        
        # Initialize git manager (real or mock based on disable_git setting)
        if not self.disable_git:
            self.git_manager = GitManager(self.version_dir)
            
            # Check if we're loading from a checkpoint (existing git repo)
            if os.path.exists(os.path.join(self.version_dir, ".git")):
                # Loading from checkpoint - load existing git repo
                self.git_manager.load_existing_repo()
            else:
                # New session - initialize new git repo
                self.git_manager.initialize_repo()
        else:
            logger.info("Git operations disabled - using mock git manager")
        
        # Only update latest symlink if this is actually the latest version
        # Check if this version is actually the latest
        versions = [int(d) for d in os.listdir(self.project_dir) if d.isdigit()]
        if versions and version.isdigit() and int(version) == max(versions):
            if os.path.islink(self.latest_dir) or os.path.isfile(self.latest_dir):
                os.unlink(self.latest_dir)
            elif os.path.isdir(self.latest_dir):
                import shutil
                shutil.rmtree(self.latest_dir)
            # Use relative path for the symlink
            version_name = os.path.basename(self.version_dir)
            os.symlink(version_name, self.latest_dir)