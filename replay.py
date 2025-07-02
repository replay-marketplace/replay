import os
import json
import argparse
import sys
import logging
from core.backend.replay import Replay, InputConfig, ReplayState, ReplayStatus

def main():
    """Main entry point for the replay CLI."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description='Process input prompts and generate code using Claude AI')
    parser.add_argument('--step', action='store_true', help='Run a single step and save state')
    parser.add_argument('--setup_only', action='store_true', help='Only setup and preprocess, do not run all steps')
    parser.add_argument('--mock', action='store_true', help='Use mock client instead of real Anthropic API')
    parser.add_argument('--version', default='latest', help='Project version to use for step mode (default: latest)')
    parser.add_argument('input_prompt_file', nargs='?', help='Path to the input prompt file (for new run)')
    parser.add_argument('project_name', nargs='?', help='Name of the project (for new run)')
    parser.add_argument('--output_dir', default='replay_output', help='Output directory (for new run)')
    args = parser.parse_args()
    
    if args.step:
        # In step mode, if only one positional argument is provided, it's the project_name
        if args.input_prompt_file and not args.project_name:
            args.project_name = args.input_prompt_file
            args.input_prompt_file = None
            
        if not args.project_name:
            logger.error("project_name is required for step mode.")
            sys.exit(1)
        try:
            runner = Replay.load_checkpoint(
                project_name=args.project_name,
                output_dir=args.output_dir,
                version=args.version,
                use_mock=args.mock
            )
        except FileNotFoundError as e:
            logger.error(f"Can't load replay from project directory: {e}")
            sys.exit(1)
        if runner.has_steps():
            runner.run_step()
            runner.save_state()
        else:
            logger.info("No more steps to run.")
            sys.exit(42)
    else:
        if not args.input_prompt_file or not args.project_name:
            logger.error("input_prompt_file and project_name are required for a new run.")
            logger.error("Usage: python replay.py <input_prompt_file> <project_name> [--output_dir <dir>]")
            sys.exit(1)
        input_config = InputConfig(
            input_prompt_file=args.input_prompt_file,
            project_name=args.project_name,
            output_dir=args.output_dir
        )
        runner = Replay.from_recipe(input_config, use_mock=args.mock)
        if args.setup_only:
            runner.compile()
            runner.save_state()
        else:
            runner.run_all()
            runner.save_state()

if __name__ == "__main__":
    main()
