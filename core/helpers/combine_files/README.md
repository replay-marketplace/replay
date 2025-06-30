# Combine Files

A simple Python utility that combines multiple files into a single output file while preserving their order.

## Usage

```bash
python combine_files.py [input_files...] --output-dir OUTPUT_DIR --output-filename OUTPUT_FILENAME
```

### Arguments

- `input_files`: One or more input files to combine (required)
- `--output-dir` or `-o`: Directory where the output file will be created (required)
- `--output-filename` or `-f`: Name of the output file (required)

### Example

```bash
# Combine three text files into a single output file
python combine_files.py file1.txt file2.txt file3.txt --output-dir output --output-filename combined.txt

# Using short options
python combine_files.py file1.txt file2.txt file3.txt -o output -f combined.txt
```

## Features

- Combines multiple files in the specified order
- Creates output directory if it doesn't exist
- Handles UTF-8 encoding
- Adds newlines between files if needed
- Provides error handling for individual files
- Preserves file order as specified in the command line

## Requirements

- Python 3.x
- No external dependencies required 