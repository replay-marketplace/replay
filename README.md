# Replay

This program processes input prompts using Claude AI and generates code based on the responses.


## Features

- **Prompt Preprocessing**: Advanced IR-based prompt processing with graph-based execution
- **Step-by-Step Execution**: Execute prompts step by step with state persistence
- **Template Processing**: Support for code templates and file generation
- **Conditional Logic**: Built-in support for conditional execution and loops
- **Code Generation**: Generate and run code with automatic testing
- **State Management**: Persistent state for resuming interrupted executions

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

# Run a prompt file
python replay.py input_prompt.txt my_project

# Run step by step
python replay.py --step --session_folder replay_output/my_project/latest input_prompt.txt my_project
```

### Programmatic Usage

```python
from core import Replay, InputConfig

# Create configuration
config = InputConfig(
    input_prompt_file="my_prompt.txt",
    project_name="my_project",
    output_dir="output"
)

# Create and run replay
replay = Replay(input_config=config)
replay.run_all()
```

## Project Structure

```
replay/
├── core/                          # Main package
│   ├── backend/                   # Execution engine
│   │   ├── replay.py             # Main Replay class
│   │   ├── registry.py           # Node processor registry
│   │   └── *_node_processor.py   # Node processors
│   ├── prompt_preprocess2/        # Prompt preprocessing
│   │   ├── processor3.py         # Main processor
│   │   ├── ir/                   # Intermediate representation
│   │   └── passes/               # Graph transformation passes
│   ├── code_to_json/             # Code to JSON conversion
│   ├── json_to_code/             # JSON to code conversion
│   └── dir_preprocessing/        # Directory setup utilities
├── examples/                      # Usage examples
├── tests/                         # Test suite
├── input_const/                   # Input constants and templates
├── replay_output/                 # Generated output
├── pyproject.toml                 # Project configuration
└── replay.py                      # CLI entry point
```

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





## Examples

### Basic Example

See `examples/basic_usage.py` for a simple example of using the replay package.

### Step-by-Step Execution

See `examples/step_by_step_execution.py` for an example of executing prompts step by step.

### Running Examples

```bash
# Run basic example
python examples/basic_usage.py

# Run step-by-step example
python examples/step_by_step_execution.py
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
from core import InputConfig

config = InputConfig(
    input_prompt_file="prompt.txt",    # Path to prompt file
    project_name="my_project",         # Project name
    output_dir="output"                # Output directory
)
```





## License

This project is licensed under the MIT License - see the LICENSE file for details.

