# JSON to Code Generator

This tool generates files from JSON input based on a specified schema. The input JSON should follow the format defined in `input_const/agent_reply_schema.json`.

## Usage

You can use this tool in two ways:

### 1. Command Line Interface

```bash
python3 json_to_code.py <output_directory> <input_json_file>
```

Example:
```bash
python3 json_to_code.py ./output ./tests/test1.json
```

### 2. Python Module

```python
from json_to_code import json_to_code

# Load your JSON data
with open('input.json', 'r') as f:
    json_data = json.load(f)

# Generate files
json_to_code('output_directory', json_data)
```

## Input JSON Format

The input JSON should be an array of objects, where each object has:
- `path_and_filename`: The full path and filename where the file should be created
- `contents`: The contents of the file

Example:
```json
[
    {
        "path_and_filename": "src/main.py",
        "contents": "def main():\n    print('Hello')\n"
    }
]
```

## Running Tests

To run the tests:
```bash
python3 -m unittest tests/test_json_to_code.py
``` 