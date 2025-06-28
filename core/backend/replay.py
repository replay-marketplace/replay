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
        session_folder: str = None
    ):
        if state is not None:
            self.state = state
        elif input_config is not None:
            self.state = ReplayState(input_config=input_config)
        else:
            raise ValueError("Must provide either input_config or state")
        self.client = client
        self.code_dir = None
        self.replay_dir = None
        self.ro_dir = None
        self.project_dir = None
        self.latest_dir = None
        self.epic_dir = session_folder
        self.system_instructions = None
        self.epic = None
        self.node_processor_registry = NodeProcessorRegistry.create_registry()

    def setup(self, clear_terminal: bool = False):
        if self.state.init.setup_done:
            return
        if clear_terminal:
            os.system('cls' if os.name == 'nt' else 'clear')
        self._init_client()
        self._load_system_instructions()
        self._setup_directories()
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
        state_path = os.path.join(self.epic_dir, "replay_state.json")
        with open(state_path, 'w') as f:
            json.dump(self.state.to_dict(), f, indent=2) 

    def preprocess(self):
        if not self.state.init.setup_done:
            self.setup()
        self.epic = prompt_preprocess3(self.state.input_config.input_prompt_file, self.replay_dir)
        self.dfs_nodes = list(nx.dfs_preorder_nodes(self.epic.graph, self.epic.first_node))
        self.state.execution.current_node_idx = 0
        self.state.init.preprocess_done = True
        self.state.execution.finished = False

    def has_steps(self):
        return self.state.execution.current_node_idx < len(self.dfs_nodes) and not self.state.execution.finished

    def _init_client(self):
        if self.client is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)

    def _load_system_instructions(self):
        try:
            with open("input_const/client_instructions_with_json.txt", "r") as f:
                self.system_instructions = f.read()
        except FileNotFoundError:
            raise RuntimeError("System instructions file not found.")

    def _setup_directories(self):
        if self.epic_dir is None:
            (self.code_dir, self.replay_dir, self.ro_dir, self.project_dir,
             self.latest_dir, self.epic_dir) = setup_project_directories(
                self.state.input_config.output_dir, self.state.input_config.project_name)
        else:
            self.code_dir = os.path.join(self.epic_dir, "code")
            self.replay_dir = os.path.join(self.epic_dir, "replay")
            self.ro_dir = os.path.join(self.epic_dir, "read_only")
            self.project_dir = os.path.dirname(self.epic_dir)
            self.latest_dir = os.path.join(self.project_dir, "latest")