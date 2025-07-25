#!/bin/bash

# Demo script for running replay on create_new_op_from_generic.txt prompt
# This script demonstrates how to use replay to generate code for an acos operation

set -e  # Exit on any error


# Parse command line arguments
CLEAN_MODE=false
OP_NAME=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN_MODE=true
            shift
            ;;
        --op)
            OP_NAME="$2"
            shift
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--clean]"
            exit 1
            ;;
    esac
done

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROMPT_FILE="$PROJECT_ROOT/examples/prompts/combine_op_llk_template.txt"
PROJECT_NAME="create_$OP_NAME"
OUTPUT_DIR="$PROJECT_ROOT/examples/demos"
NEW_PROMPT_FILE="$(dirname "$PROMPT_FILE")/$OP_NAME""_prompt.txt"

echo "=== Replay Demo: New OP ==="
echo "Prompt file: $PROMPT_FILE"
echo "Project name: $PROJECT_NAME"
echo "Output directory: $OUTPUT_DIR"
echo "Clean mode: $CLEAN_MODE"
echo "New prompt file: $NEW_PROMPT_FILE"
echo ""

# Check if prompt file exists
if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: Prompt file not found at $PROMPT_FILE"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# If clean mode is enabled, remove the project output folder
if [ "$CLEAN_MODE" = true ]; then
    if [ -d "$OUTPUT_DIR/$PROJECT_NAME" ]; then
        echo "Cleaning previous output directory: $OUTPUT_DIR/$PROJECT_NAME"
        rm -rf "$OUTPUT_DIR/$PROJECT_NAME"
    fi
fi

# Change to project root directory
cd "$PROJECT_ROOT"

echo "Starting replay execution..."
echo "Command: python3 replay.py \"$PROMPT_FILE\" \"$PROJECT_NAME\" --output_dir \"$OUTPUT_DIR\""
echo ""

# Create the project output directory for logging
mkdir -p "$OUTPUT_DIR/$PROJECT_NAME"

# Create prompt from template
python3 update_template.py "$PROMPT_FILE" "$OP_NAME" "$NEW_PROMPT_FILE"

PROMPT_FILE="$NEW_PROMPT_FILE"
echo "PWD:"
pwd

# Run the replay with logging
python3 replay.py "$PROMPT_FILE" "$PROJECT_NAME" --output_dir "$OUTPUT_DIR" 2>&1 | tee "$OUTPUT_DIR/log.txt"

echo ""
echo "=== Demo completed ==="
echo "Check the output in: $OUTPUT_DIR/$PROJECT_NAME"
echo "Log file: $OUTPUT_DIR/$PROJECT_NAME/log.txt" 
