# Preprocessing Passes

The passes system is a key component of the prompt preprocessing pipeline. It transforms the intermediate representation (EpicIR) through a series of compilation passes, each handling specific aspects of lowering high-level constructs into executable operations.

## Overview

Passes operate on the EpicIR graph structure, transforming it from parsed prompt text into a fully executable workflow. The system follows a **pipeline architecture** where:

1. **Input**: EpicIR graph with high-level constructs
2. **Transformation**: Series of passes that lower, optimize, and enhance the graph  
3. **Output**: Executable IR ready for backend processing

Each pass is designed to handle a specific transformation, making the system modular and maintainable.

## Pass Architecture

### Pass Function Signature
All passes follow a consistent interface:

```python
def pass_name(epic: EpicIR) -> EpicIR:
    """Transform the EpicIR and return the modified version."""
    # Transformation logic
    return epic
```

### Pass Registry System
The `PassRegistry` manages pass execution order and metadata:

```python
from pass_registry import PassRegistry

registry = PassRegistry()
registry.register(pass_lower_debug_loop, name="lower_debug_loop")
registry.register(pass_insert_exit_node, name="insert_exit_node")

# Execute all passes in order
for pass_info in registry.get_all_passes():
    epic = pass_info.func(epic)
```

## Available Passes

### 1. `pass_lower_debug_loop.py`

**Purpose**: Transform high-level DEBUG_LOOP constructs into concrete retry mechanisms.

**Transformation**:
```
DEBUG_LOOP(command="make test")
    ↓
RUN(command="make test") → CONDITIONAL → [success]
    ↑                          ↓
    └─────── FIX ←────────── [failure]
```

**Key Features**:
- Creates retry loops with automatic error fixing
- Configurable iteration limits (default: 5)
- Integrates with FIX nodes for intelligent error handling
- Supports single DEBUG_LOOP per graph (limitation)

**Generated Nodes**:
- **RUN**: Executes the command
- **CONDITIONAL**: Checks success/failure, manages iteration count
- **FIX**: Analyzes failures and applies corrections

**Example Input**:
```
/DEBUG_LOOP make build
```

**Example Output Graph**:
```
[previous] → RUN(make build) → CONDITIONAL → [next]
                ↑                   ↓
                └─── FIX ←─────────┘
```

### 2. `pass_insert_exit_node.py`

**Purpose**: Ensure all execution paths terminate with an EXIT node.

**Transformation**:
- Analyzes graph using breadth-first search
- Checks if EXIT node already exists
- Appends EXIT node to final node if missing

**Key Features**:
- Prevents infinite execution loops
- Ensures clean workflow termination
- Maintains graph connectivity

**Example**:
```
Before: PROMPT → RUN → (end)
After:  PROMPT → RUN → EXIT
```

### 3. `pass_lower_prompt_file_refs.py`

**Purpose**: Extract and process file references from prompt text.

**Supported Reference Types**:
- `@docs:filename` - Documentation files
- `@template:filename` - Template files  
- `@code:filename` - Code files for editing
- `@run_logs:filename` - Previous execution logs
- `@run_ref:node_id` - References to RUN node outputs

**Transformation**:
```python
# Input prompt text:
"Fix the issue in @code:main.cpp using @docs:api_guide.md"

# Generated node contents:
{
    "prompt": "Fix the issue in @code:main.cpp using @docs:api_guide.md",
    "code_refs": ["main.cpp"],
    "docs_refs": ["api_guide.md"],
    "template_refs": [],
    "run_logs_refs": []
}
```

**Key Features**:
- Regex-based reference extraction
- Support for multiple reference types
- Preserves original prompt text
- Enables file loading during execution

### 4. `pass_process_ro_markers.py`

**Purpose**: Process read-only (RO) markers in prompt text and create READ_ONLY nodes.

**Transformation**:
```
/RO shared_folder
    ↓
READ_ONLY(path="shared_folder") → PROMPT
```

**Key Features**:
- Extracts folder paths after `/RO` markers
- Creates READ_ONLY nodes for each reference
- Links READ_ONLY nodes to their consuming PROMPT nodes
- Supports multiple RO references per prompt

**Example**:
```python
# Input: "Use code from /RO utils and /RO helpers"
# Creates:
# - READ_ONLY(path="utils") → PROMPT
# - READ_ONLY(path="helpers") → PROMPT
```

### 5. `pass_registry.py`

**Purpose**: Provide infrastructure for pass management and execution.

**Key Classes**:

#### PassInfo
Encapsulates pass metadata:
```python
class PassInfo:
    func: Callable      # The pass function
    name: str          # Display name
    description: str   # What the pass does
```

#### PassRegistry  
Manages pass collection and execution order:
```python
class PassRegistry:
    def register(pass_func, name=None, description=None)
    def get(name) -> PassInfo
    def get_all_passes() -> List[PassInfo]
```

**Features**:
- Automatic name generation from function names
- Description extraction from docstrings
- Ordered execution support
- Pass introspection capabilities

## Pass Execution Pipeline

The typical pass execution order:

1. **`pass_process_ro_markers`** - Process read-only references
2. **`pass_lower_prompt_file_refs`** - Extract file references  
3. **`pass_lower_debug_loop`** - Lower high-level constructs
4. **`pass_insert_exit_node`** - Ensure proper termination

This order ensures:
- References are processed before lowering
- High-level constructs are lowered before finalization
- Graph structure is complete before execution

## Implementation Details

### Graph Traversal
Passes use NetworkX operations for graph manipulation:

```python
# Iterate through nodes
for node_id in epic.graph.nodes():
    node_data = epic.graph.nodes[node_id]
    
# Modify graph structure
epic.graph.add_node(new_node_id, opcode=Opcode.RUN, contents={})
epic.graph.add_edge(predecessor, new_node_id)
epic.graph.remove_node(old_node_id)
```

### Opcode Usage
Passes work with standardized opcodes:

```python
from ..ir.ir import Opcode

# Check node type
if node_data['opcode'] == Opcode.DEBUG_LOOP:
    # Process debug loop
    
# Create new nodes
epic.add_node(opcode=Opcode.RUN, contents={"command": cmd})
```

### Content Structure
Node contents follow consistent patterns:

```python
# RUN node
contents = {"command": "make test"}

# CONDITIONAL node  
contents = {
    "iteration_count": 0,
    "iteration_max": 5,
    "run_node_id": run_node_ref,
    "condition": False
}

# PROMPT node with references
contents = {
    "prompt": "Fix the code",
    "code_refs": ["main.cpp"],
    "docs_refs": ["guide.md"]
}
```

## Error Handling

Passes include comprehensive error handling:

```python
def pass_example(epic: EpicIR) -> EpicIR:
    try:
        # Transformation logic
        return epic
    except Exception as e:
        logger.error(f"Pass failed: {e}")
        return epic  # Return unmodified on error
```

**Common Error Scenarios**:
- Missing required node contents
- Invalid graph structure
- Multiple unsupported constructs
- Malformed references

## Debugging Passes

### Logging
All passes include detailed logging:

```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Processing {len(nodes)} nodes")
logger.debug(f"Node contents: {node_contents}")
logger.warning(f"Skipping invalid node: {node_id}")
```

### Graph Inspection
Inspect graph state before/after passes:

```python
# Before pass
print(f"Nodes: {list(epic.graph.nodes())}")
print(f"Edges: {list(epic.graph.edges())}")

# Apply pass
epic = pass_function(epic)

# After pass  
print(f"Modified nodes: {list(epic.graph.nodes())}")
```

### Visualization
NetworkX integration allows graph visualization:

```python
import networkx as nx
import matplotlib.pyplot as plt

pos = nx.spring_layout(epic.graph)
nx.draw(epic.graph, pos, with_labels=True)
plt.show()
```

## Creating Custom Passes

### 1. Basic Pass Structure

```python
def pass_my_transformation(epic: EpicIR) -> EpicIR:
    """
    Description of what this pass does.
    
    Args:
        epic: The EpicIR graph to transform
        
    Returns:
        EpicIR: The modified graph
    """
    
    # Find nodes to transform
    target_nodes = []
    for node_id in epic.graph.nodes():
        node_data = epic.graph.nodes[node_id]
        if should_transform(node_data):
            target_nodes.append(node_id)
    
    # Apply transformations
    for node_id in target_nodes:
        transform_node(epic, node_id)
    
    return epic
```

### 2. Registration

```python
# In pass registration code
from .pass_my_transformation import pass_my_transformation

registry.register(
    pass_my_transformation,
    name="my_transformation",
    description="Transforms X into Y for improved execution"
)
```

### 3. Testing

```python
def test_my_pass():
    # Create test IR
    epic = EpicIR()
    epic.graph.add_node("test", opcode=Opcode.TEST, contents={})
    
    # Apply pass
    result = pass_my_transformation(epic)
    
    # Verify transformation
    assert "new_node" in result.graph.nodes()
    assert result.graph.nodes["new_node"]["opcode"] == Opcode.EXPECTED
```

## Best Practices

### Pass Design
1. **Single Responsibility**: Each pass should handle one transformation type
2. **Idempotent**: Passes should be safe to run multiple times
3. **Conservative**: Prefer minimal changes over complex transformations
4. **Documented**: Include comprehensive docstrings and examples

### Error Handling
1. **Graceful Degradation**: Return unmodified IR on errors when possible
2. **Detailed Logging**: Log all decisions and transformations
3. **Validation**: Check preconditions before transformation
4. **Recovery**: Provide fallback behavior for edge cases

### Performance
1. **Efficient Traversal**: Use appropriate graph algorithms
2. **Minimal Copies**: Modify graphs in-place when possible  
3. **Early Exit**: Skip unnecessary work when possible
4. **Memory Management**: Clean up temporary data structures

## File Organization

```
core/prompt_preprocess2/passes/
├── README.md                      # This file
├── __init__.py                    # Package initialization
├── pass_registry.py               # Pass management infrastructure
├── pass_lower_debug_loop.py       # DEBUG_LOOP → RUN/CONDITIONAL/FIX
├── pass_insert_exit_node.py       # Ensure EXIT node present
├── pass_lower_prompt_file_refs.py # Extract @file references
└── pass_process_ro_markers.py     # Process /RO markers
```

## Integration

Passes integrate with the broader preprocessing pipeline:

1. **Parser** → Creates initial EpicIR from prompt text
2. **Passes** → Transform and optimize the IR  
3. **Backend** → Executes the final IR graph

The pass system sits between parsing and execution, providing the crucial transformation layer that makes high-level prompt constructs executable. 