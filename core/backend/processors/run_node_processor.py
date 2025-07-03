import os
import subprocess
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class RunNodeProcessor:
    """
    Processor for RUN nodes in the workflow.
    
    The RunNodeProcessor executes shell commands specified in RUN nodes and captures
    their output, exit codes, and logs. This is a critical component for running
    build commands, tests, and other system operations during replay execution.
    
    Key responsibilities:
    - Execute shell commands in the specified working directory
    - Capture stdout and stderr streams
    - Record exit codes for conditional branching
    - Save command output to timestamped log files
    - Update replay memory with execution results
    
    The processor saves all command output to timestamped files in the run_logs directory
    for later analysis and debugging.
    """
    
    def process(self, replay, node: dict) -> None:
        """
        Process a RUN node by executing the specified command.
        
        This method extracts the command from the node contents, executes it in the
        replay's code directory, and captures all output. The results are saved to
        log files and the node contents are updated with the exit code and file paths.
        
        Args:
            replay: The Replay instance containing execution state and directories
            node (dict): The RUN node containing the command to execute
            
        Raises:
            ValueError: If no command is found in the node contents
            
        Side Effects:
            - Updates node contents with exit_code, stdout_file, stderr_file
            - Creates timestamped log files in replay.run_logs_dir
            - Updates replay.state.execution.memory with execution results
        """
        node_id = node.get('id', 'UNKNOWN')
        
        # Get the command from node contents
        contents = node['contents']
        command_to_run = contents.get('command', '')
        if not command_to_run:
            raise ValueError(f"No command found in node contents: {node_id}")      
            
        logger.info(f"Running command {node_id}: \n{command_to_run} \nin {replay.code_dir}")
        
        # Run the command and capture the exit code
        try:
            result = subprocess.run(command_to_run, shell=True, cwd=replay.code_dir, 
                                  capture_output=True, text=True)
            exit_code = result.returncode
            
            # Store the exit code in node contents
            contents['exit_code'] = exit_code
            
            def write_to_file(result_text: str, node: dict, suffix: str) -> str:
                """
                Write command output to a timestamped file.
                
                Args:
                    result_text (str): The command output to write
                    node (dict): The node being processed (for filename generation)
                    suffix (str): File suffix ('stdout' or 'stderr')
                    
                Returns:
                    str: The filename of the created file (relative to run_logs_dir)
                """
                now = datetime.now().strftime("%H-%M-%S-%f")
                file_name = f"{os.path.basename(str(node_id))}_{suffix}_{now}.txt"                
                file_path = os.path.join(replay.run_logs_dir, file_name)
                with open(file_path, "w") as f:
                    f.write(result_text)
                
                logger.info(f"Wrote {suffix} to file: {file_path}")
                logger.debug(f"Contents of {suffix} file: \n{result_text}")

                return file_name

            # Save stdout if not empty
            if result.stdout.strip() != "":
                file_path = write_to_file(result.stdout, node, "stdout")
                contents['stdout_file'] = file_path

            # Save stderr if not empty
            if result.stderr.strip() != "":
                file_path = write_to_file(result.stderr, node, "stderr")
                contents['stderr_file'] = file_path  
            
            # Update replay memory with execution results
            if exit_code != 0:
                replay.state.execution.memory.append(f"Command `{command_to_run}` failed with exit code {exit_code}. Stderr file: {file_path}")
            else:
                replay.state.execution.memory.append(f"Command `{command_to_run}` completed successfully")
            
            logger.info(f"Command completed with exit code: {exit_code}")
            
        except Exception as e:
            logger.error(f"Error running command': {e}")
            contents['exit_code'] = -1