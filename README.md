# Replay Program

This program processes input prompts using Claude AI and generates code based on the responses.

## Prerequisites

- Python 3.x
- Anthropic API key (set as environment variable `ANTHROPIC_API_KEY`)

## Installation

1. Install the required dependencies:
```bash
pip install anthropic
```

2. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

Run the replay program using the following command:

```bash
python3 replay.py <input_prompt_file> <project_name>
```

Example:
```bash
python3 replay.py input_prompt.txt my_project
```

The program will:
1. Create necessary directories in `replay_output/`
2. Process the input prompt
3. Generate code based on Claude's responses
4. Save all outputs in the project directory

## Running Tests

To run the tests:

```bash
python3 -m pytest tests/
```

## Directory Structure

- `replay_output/<project_name>/` - Contains replay data and generated code
  - `input_prompt.txt` - Copy of the input prompt
  - `prompt.json` - Processed prompt in JSON format
  - `code/` - Generated code files 