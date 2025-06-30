import os
import subprocess
import logging

logger = logging.getLogger(__name__)

class RunNodeProcessor:
    def process(self, replay, node):
        logger.debug(f"node: {node}")
        command_to_run = "chmod 755 run_tests.sh"
        subprocess.run(command_to_run, shell=True, cwd=replay.code_dir)
        command_to_run = replay.state.execution.epic.graph.nodes[node]['contents']['command_to_run']
        logger.debug(f"GOING TO RUN COMMAND: {command_to_run}")
        subprocess.run(command_to_run, shell=True, cwd=replay.code_dir)
        with open(os.path.join(replay.replay_dir, "run_tests_pass_fail.txt"), "r") as f:
            replay.state.execution.epic.graph.nodes[node]['contents']['passed'] = f.read()
        logger.debug(f"Test results: {replay.state.execution.epic.graph.nodes[node]['contents']['passed']}") 