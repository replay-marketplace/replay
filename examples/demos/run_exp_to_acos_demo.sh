#!/bin/bash

# Demo script for running replay on create_new_op_from_generic.txt prompt
# This script demonstrates how to use replay to generate code for an acos operation

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROMPT_FILE="$PROJECT_ROOT/examples/prompts/create_new_op_from_generic.txt"
PROJECT_NAME="exp_to_acos"
OUTPUT_DIR="$PROJECT_ROOT/examples/demos"

echo "=== Replay Demo: exp_to_acos ==="
echo "Prompt file: $PROMPT_FILE"
echo "Project name: $PROJECT_NAME"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Check if prompt file exists
if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: Prompt file not found at $PROMPT_FILE"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Change to project root directory
cd "$PROJECT_ROOT"

echo "Starting replay execution..."
echo "Command: python replay.py \"$PROMPT_FILE\" \"$PROJECT_NAME\" --output_dir \"$OUTPUT_DIR\""
echo ""

# Run the replay
python replay.py "$PROMPT_FILE" "$PROJECT_NAME" --output_dir "$OUTPUT_DIR"

echo ""
echo "=== Demo completed ==="
echo "Check the output in: $OUTPUT_DIR/$PROJECT_NAME" 