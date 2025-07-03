import json
import logging
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from core.prompt_preprocess2.ir.ir import Opcode

logger = logging.getLogger(__name__)

@dataclass
class FileReference:
    """Represents a file reference with path and content."""
    path: str
    content: str

@dataclass
class LLMRequest:
    """Represents an LLM request with prompt and file references."""
    prompt: str
    code_to_edit: List[FileReference]
    read_only_files: List[FileReference]
    run_logs_files: List[FileReference]
    memory: List[str]

class FixNodeProcessor:
    """Processes FIX nodes by analyzing run logs and applying fixes to code."""
    
    # Configuration constants
    DEFAULT_MODEL = "claude-3-7-sonnet-20250219"
    DEFAULT_MAX_TOKENS = 10000
    LAST_N_ERROR_LINES = 100
    CLIENT_INSTRUCTIONS_FILE = "client_instructions_with_json.txt" #"client_instructions_indentify_issue.txt"
    
    def process(self, replay, node: dict) -> None:
        """
        Process a FIX node by analyzing the referenced RUN node's logs and applying fixes.
        
        Args:
            replay: The replay instance containing state and client
            node: The node data dictionary to process
        """
        try:
            logger.info(f"Processing FIX node {node}")
            
            # Extract the run reference from node contents
            contents = node.get('contents', {})
            run_ref = contents.get('run_ref', None)
            
            if run_ref is None:
                raise ValueError(f"No run_ref found in FIX node: {node}")
            
            # Get the referenced RUN node
            run_node = replay.state.execution.epic.graph.nodes[run_ref]
            run_node_opcode = run_node.get('opcode')
            if run_node_opcode != Opcode.RUN:
                raise ValueError(f"Referenced node {run_ref} is not a RUN node but {run_node_opcode}")
            
            # Extract run logs from the RUN node
            stderr_file, stdout_file = self._extract_run_log_files(run_node, replay)
            stderr_file_content = self._load_files_from_directory([stderr_file], replay.run_logs_dir, "stderr file", last_n_lines=self.LAST_N_ERROR_LINES)
            run_logs_files = self._load_files_from_directory([stderr_file], replay.run_logs_dir, "run log file", last_n_lines=self.LAST_N_ERROR_LINES)
            logger.info(f"Found attached run logs files: {run_logs_files}")

            # Get relevant code files mentioned in the logs
            # Use stderr for error analysis, but could be enhanced to use both
            log_file_for_analysis = stderr_file if stderr_file else stdout_file            
            relevant_code_files_contents = []
            if log_file_for_analysis:
                relevant_code_files = self._get_relevant_code_files(log_file_for_analysis, replay)
                relevant_code_files_contents = self._load_files_from_directory(relevant_code_files, replay.code_dir, "code file")            
                

            # Build and send LLM request
            llm_request = self._build_llm_request(run_logs_files, relevant_code_files_contents, replay)
            response_data = self._send_llm_request(replay, llm_request)
            
            # Apply fixes based on LLM response
            self._process_generic_llm_response(response_data, replay)
            
            logger.info(f"Processed FIX node {node}")
            
        except Exception as e:
            logger.error(f"Error processing FIX node {node}: {e}")
            raise

    # returns a tuple of two lists: [stderr_file, stdout_file]
    def _extract_run_log_files(self, run_node: dict, replay) -> tuple[str, str]:
        """Extract run logs from a RUN node."""
        run_node_contents = run_node.get('contents', {})
        
        # Get stderr and stdout files
        stderr_file = run_node_contents.get('stderr_file', None)
        stdout_file = run_node_contents.get('stdout_file', None)
        
        return stderr_file, stdout_file

    # returns a list of file names that are mentioned in the log file
    def _get_relevant_code_files(self, log_file: str, replay) -> List[str]:
        """Get code files that are mentioned in the run logs."""
        # Get all file names from code folder
        code_dir = replay.code_dir
        run_logs_dir = replay.run_logs_dir
        code_files = []        
        if os.path.exists(code_dir):
            logger.info(f"Found code files in {code_dir}")
            for file_name in os.listdir(code_dir):
                logger.info(f"Found code file: {file_name}")
                if os.path.isfile(os.path.join(code_dir, file_name)):
                    logger.info(f"Its a file: {file_name}")
                    code_files.append(file_name)
        
        relevant_code_files = []
        log_content = self._read_file_safely(os.path.join(run_logs_dir, log_file), last_n_lines=self.LAST_N_ERROR_LINES)
        logger.info(f"Log content: {log_content}")
        for file_name in code_files:
            logger.info(f"Checking if {file_name} is in log content")
            if file_name in log_content:
                logger.info(f"Found {file_name} in log content")
                relevant_code_files.append(file_name)
            else:
                logger.info(f"Did not find {file_name} in log content")
        
        return relevant_code_files

    def _load_files_from_directory(self, file_refs: List[str], base_dir: str, file_type: str, last_n_lines: int = None) -> List[FileReference]:
        """Load files from a directory and return FileReference objects."""
        files = []
        
        for file_ref in file_refs:
            file_path = os.path.join(base_dir, file_ref)
            
            if os.path.exists(file_path):
                try:
                    content = self._read_file_safely(file_path, last_n_lines)
                    files.append(FileReference(path=file_ref, content=content))
                    logger.info(f"Added {file_type} to edit: {file_ref}")
                except Exception as e:
                    logger.error(f"Error reading {file_type} {file_path}: {e}")
            else:
                logger.warning(f"{file_type.title()} not found: {file_path}")
        
        return files

    def _build_llm_request(self, run_logs_files: List[FileReference], code_files: List[FileReference], replay) -> LLMRequest:
        """Build the LLM request for analysis."""
        prompt = "Review the error logs and suggest fixes for the code files."
        
        return LLMRequest(
            prompt=prompt,
            code_to_edit=code_files,
            read_only_files=[],
            run_logs_files=run_logs_files,
            memory=replay.state.execution.memory # use memory from replay state
        )

    def _send_llm_request(self, replay, llm_request: LLMRequest) -> Dict[str, Any]:
        """Send the LLM request and return the parsed response."""
        # Convert to JSON format expected by LLM
        request_dict = {
            "prompt": llm_request.prompt,
            "run_logs_files": [{"path_and_filename": f.path, "contents": f.content} for f in llm_request.run_logs_files],
            "code_to_edit": [{"path_and_filename": f.path, "contents": f.content} for f in llm_request.code_to_edit],
            "memory": llm_request.memory
        }
        request_json = json.dumps(request_dict, indent=2)
        
        logger.info(f"Sending FIX request to LLM with {len(llm_request.run_logs_files)} run logs files and {len(llm_request.code_to_edit)} code files")
        
        # Get client instructions
        system_prompt = self._get_client_instructions(replay.replay_dir)
        
        # Send to LLM
        response = replay.client.messages.create(
            model=self.DEFAULT_MODEL,
            max_tokens=self.DEFAULT_MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": request_json}]
        )
        
        # Parse response
        response_content = response.content[0].text
        
        try:
            return json.loads(response_content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Response content: {response_content}")
            raise

    def _process_generic_llm_response(self, response_data: Dict[str, Any], replay) -> None:
        """Process the LLM response and save generated files."""
        if 'files' in response_data:
            for file_data in response_data['files']:
                file_path = file_data.get('path_and_filename', '')
                file_content = file_data.get('contents', '')
                
                if file_path and file_content:
                    self._save_generated_file(file_path, file_content, replay.code_dir)
        if 'memory' in response_data:
            replay.state.execution.memory = response_data['memory']
            logger.info(f"Updated memory: \n{replay.state.execution.memory}")

    def _save_generated_file(self, file_path: str, content: str, code_dir: str) -> None:
        """Save a generated file to the code directory."""
        full_path = os.path.join(code_dir, file_path)
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Write file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Saved updated file: {full_path}")
            
        except Exception as e:
            logger.error(f"Error saving generated file {full_path}: {e}")
            raise     

    def _read_file_safely(self, file_path: str, last_n_lines: int = None) -> str:
        """Read a file safely with proper encoding handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if last_n_lines is not None:
                    return '\n'.join(f.readlines()[-last_n_lines:])
                else:
                    return f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return ""

    def _get_client_instructions(self, replay_dir: str) -> str:
        """Load client instructions from the replay directory."""
        instructions_path = os.path.join(replay_dir, self.CLIENT_INSTRUCTIONS_FILE)
        
        if os.path.exists(instructions_path):
            try:
                return self._read_file_safely(instructions_path)
            except Exception as e:
                raise Exception(f"Error reading client instructions from {instructions_path}: {e}")
        else:
            raise FileNotFoundError(f"Client instructions file not found: {instructions_path}") 