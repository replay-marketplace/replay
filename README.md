# Replay

This program processes input prompts using Claude AI and generates code based on the responses.


## Features

- **Prompt Preprocessing**: Advanced IR-based prompt processing with graph-based execution
- **Step-by-Step Execution**: Execute prompts step by step with state persistence
- **Template Processing**: Support for code templates and file generation
- **Conditional Logic**: Built-in support for conditional execution and loops
- **Code Generation**: Generate and run code with automatic testing
- **State Management**: Persistent state for resuming interrupted executions
- **Versioned Output**: Each run is saved in a numbered versioned directory, with a `latest` symlink for convenience

## Installation

### From PyPI (when published)
```bash
pip install replay
```

### From Source
```bash
git clone <repository-url>
cd replay
pip install -e .
```

### Development Installation
```bash
pip install -e ".[dev]"
```

## Prerequisites

- Python 3.8 or higher
- Anthropic API key (set as environment variable `ANTHROPIC_API_KEY`)

## Quick Start

### Command Line Usage

```bash
# Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Run a prompt file (creates a new versioned run)
python replay.py input_prompt.txt my_project --output_dir replay_output

# Run step by step (using the latest version by default)
python replay.py my_project --output_dir replay_output --step

# To select a specific version (e.g., version 2):
python replay.py my_project --output_dir replay_output --step --version 2
```

- All outputs are saved under `replay_output/<project_name>/<version>/`.
- The symlink `replay_output/<project_name>/latest` always points to the most recent version.

### Programmatic Usage

```python
from core.backend.replay import Replay, InputConfig

# Create configuration
config = InputConfig(
    input_prompt_file="my_prompt.txt",
    project_name="my_project",
    output_dir="output"
)

# Create and run replay
replay = Replay.from_recipe(config)
replay.run_all()
```

## Output Directory Structure

```
replay_output/
└── my_project/
    ├── 1/                # First run (version 1)
    │   ├── code/
    │   ├── docs/
    │   ├── template/
    │   └── replay/
    │       ├── replay_state.json
    │       ├── epic.png
    │       ├── epic.txt
    │       ├── passes/
    │       └── ...
    ├── 2/                # Second run (version 2)
    │   └── ...
    └── latest -> 2/      # Symlink to latest version
```

- Each run creates a new numbered version directory.
- The `latest` symlink always points to the most recent version.
- All intermediate and final files are saved under the appropriate version directory.

## Development

### Setup Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=core --cov-report=html --cov-report=term-missing

# Run only fast tests (exclude slow markers)
pytest -m "not slow"

# Run specific test markers
pytest -m unit      # Unit tests only
pytest -m integration  # Integration tests only
```





## Prompt Format

The replay system supports a rich prompt format with special markers:

### Basic Markers

- `/TEMPLATE` - Define code templates
- `/RUN` - Execute commands
- `/RO` - Read-only file references


## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY` - Required Anthropic API key

### Input Configuration

```python
from core.backend.replay import InputConfig

config = InputConfig(
    input_prompt_file="prompt.txt",    # Path to prompt file
    project_name="my_project",         # Project name
    output_dir="output"                # Output directory
)
```





## License

This project is licensed under the MIT License - see the LICENSE file for details.

