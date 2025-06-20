# Prompt Preprocessing Tool

This tool processes text files containing prompts (separated by `\PROMPT`) and converts them into JSON format.

## Usage

### Command Line

To process a text file from the command line:

```bash
python3 -m core.prompt_preprocessing.prompt_preprocessing input_file.txt output_directory
```

Example:
```bash
python3 -m core.prompt_preprocessing.prompt_preprocessing sample.txt ./output
```

### Input File Format

The input text file should contain prompts separated by `\PROMPT`. For example:

```
This is the first prompt
It has multiple lines
\PROMPT
This is the second prompt
It also has multiple lines
```

### Output

The tool will create a JSON file in the specified output directory. The JSON file will contain an array of prompt objects, each with the following structure:

```json
[
  {
    "type": "prompt",
    "contents": "This is the first prompt\nIt has multiple lines"
  },
  {
    "type": "prompt",
    "contents": "This is the second prompt\nIt also has multiple lines"
  }
]
```

## Running Tests

To run the test suite:

```bash
python3 -m unittest discover core/prompt_preprocessing/tests
``` 