import os
import json
import argparse
import sys
import logging
from core.backend.replay import Replay, InputConfig, ReplayState

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description='Process input prompts and generate code using Claude AI')
    parser.add_argument('--session_folder', default=None, help='Path to the session (run) folder for step mode')
    parser.add_argument('--step', action='store_true', help='Run a single step and save state')
    parser.add_argument('input_prompt_file', nargs='?', help='Path to the input prompt file (for new run)')
    parser.add_argument('project_name', nargs='?', help='Name of the project (for new run)')
    parser.add_argument('--output_dir', default='replay_output', help='Output directory (for new run)')
    args = parser.parse_args()
    if args.step:
        if not args.session_folder:
            logger.error("--session_folder is required for step mode.")
            sys.exit(1)
        state_path = os.path.join(args.session_folder, "replay_state.json")
        with open(state_path, 'r') as f:
            state = ReplayState.from_dict(json.load(f))
        runner = Replay(state=state, session_folder=args.session_folder)
        if runner.state.execution.current_node_idx < len(runner.state.init.dfs_nodes) and not runner.state.execution.finished:
            runner.run_step()
            runner.save_state()
            logger.info(f"Step complete. State saved to {os.path.join(args.session_folder, 'replay_state.json')}")
        else:
            logger.info("No more steps to run.")
    else:
        if not args.input_prompt_file or not args.project_name:
            logger.error("input_prompt_file and project_name are required for a new run.")
            sys.exit(1)
        input_config = InputConfig(
            input_prompt_file=args.input_prompt_file,
            project_name=args.project_name,
            output_dir=args.output_dir
        )
        runner = Replay(input_config=input_config)
        runner.run_all()
        runner.save_state()
