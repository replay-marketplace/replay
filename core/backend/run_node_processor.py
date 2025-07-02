import os
import subprocess
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RunNodeProcessor:
    def process(self, replay, node):
        logger.debug(f"node: {node}")
        
        # Get the command from node contents
        contents = node['contents']
        command_to_run = contents.get('command', '')
        if not command_to_run:
            raise ValueError(f"No command found in node contents: {node}")      
            
        logger.debug(f"GOING TO RUN COMMAND: {command_to_run} in {replay.code_dir}")
        
        # Run the command and capture the exit code
        try:
            result = subprocess.run(command_to_run, shell=True, cwd=replay.code_dir, 
                                  capture_output=True, text=True)
            exit_code = result.returncode
            
            # Store the exit code in node contents
            contents['exit_code'] = exit_code
            
            # returns path relative to replay.run_logs_dir
            def write_to_file(result, node, suffix):
                now = datetime.now().strftime('%H-%M-%S')
                file_name = f"{os.path.basename(contents['id'])}_{suffix}_{now}.txt"                
                file_path = os.path.join(replay.run_logs_dir, file_name)
                with open(file_path, "w") as f:
                    f.write(result)
                
                logger.info(f"Wrote {suffix} to file: {file_path}")
                logger.debug(f"Contents of {suffix} file: \n{result}")

                return file_name

            if result.stdout.strip() != "":
                file_path = write_to_file(result.stdout, node, "stdout")
                contents['stdout_file'] = file_path

            if result.stderr.strip() != "":
                file_path = write_to_file(result.stderr, node, "stderr")
                contents['stderr_file'] = file_path
            
            logger.info(f"Command completed with exit code: {exit_code}")
            
        except Exception as e:
            logger.error(f"Error running command '{command_to_run}': {e}")
            contents['exit_code'] = -1