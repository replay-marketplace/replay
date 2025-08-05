import json
import logging
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .llm_backend import LLMBackend

logger = logging.getLogger(__name__)


@dataclass
class FileReference:
    """Represents a file reference with path and content."""
    path: str
    content: str


class AnthropicAPIBackend(LLMBackend):
    """
    Anthropic API backend implementation that uses the standard Anthropic client.
    
    This implementation follows the patterns from origin/main processors,
    where file contents are included in full in the requests rather than
    just file paths.
    """
    
    DEFAULT_MAX_TOKENS = 10000
    CLIENT_INSTRUCTIONS_FILE = "client_instructions_with_json.txt"
    
    def __init__(self, model_name: str = "claude-3-7-sonnet-20250219", client=None):
        """
        Initialize the Anthropic API backend.
        
        Args:
            model_name: The model name (without anthropic/ prefix for standard API)
            client: Optional pre-configured client. If None, will be provided by replay context.
        """
        super().__init__(model_name)
        
        self.client = client  # Will be set by replay context
        
        logger.info(f"Initialized AnthropicAPIBackend with model: {self.model_name}")
    
    def package_files_with_contents(self, code_files: List[FileReference], 
                                  read_only_files: List[FileReference],
                                  run_logs_files: List[FileReference] = None,
                                  memory: List[str] = None) -> Dict[str, Any]:
        """
        Package files for an LLM request with full file contents.
        
        This follows the origin/main pattern where file contents are included
        in the request rather than just file paths.
        
        Args:
            code_files: Files that can be edited
            read_only_files: Files that are read-only (docs, templates, etc.)  
            run_logs_files: Run log files (optional)
            memory: Memory items (optional)
            
        Returns:
            Dict containing the packaged request data with full file contents
        """
        request_data = {
            "code_to_edit": [{"path_and_filename": f.path, "contents": f.content} for f in code_files],
            "read_only_files": [{"path_and_filename": f.path, "contents": f.content} for f in read_only_files],
        }
        
        if run_logs_files:
            request_data["run_logs_files"] = [{"path_and_filename": f.path, "contents": f.content} for f in run_logs_files]
            
        if memory:
            request_data["memory"] = memory
            
        return request_data
    
    def load_files_from_directory(self, file_refs: List[str], base_dir: str, 
                                file_type: str, last_n_lines: int = None) -> List[FileReference]:
        """
        Load files from a directory and return FileReference objects.
        
        This follows the exact pattern from the origin/main processors.
        """
        files = []
        
        for file_ref in file_refs:
            file_path = os.path.join(base_dir, file_ref)
            
            if os.path.exists(file_path):
                try:
                    content = self._read_file_safely(file_path, last_n_lines)
                    files.append(FileReference(path=file_ref, content=content))
                    logger.info(f"Added {file_type}: {file_ref}")
                except Exception as e:
                    logger.error(f"Error reading {file_type} {file_path}: {e}")
            else:
                logger.warning(f"{file_type.title()} not found: {file_path}")
        
        return files
    
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
    
    def send_request(self, prompt: str, files_json: str, system_prompt: str = None) -> Dict[str, Any]:
        """
        Send a request to the Anthropic API.
        
        This follows the pattern established in the origin/main processors.
        
        Args:
            prompt: The user prompt
            files_json: JSON string containing the request data with full file contents
            system_prompt: Optional system prompt
            
        Returns:
            Dict containing the parsed LLM response
        """
        if not self.client:
            raise RuntimeError("Client not configured. This backend should be used within a replay context.")
        
        logger.info(f"Sending request to {self.model_name}")
        
        # Build the message content - either just the prompt or prompt + files
        if files_json and files_json.strip():
            try:
                # Try to parse files_json to see if it contains actual data
                files_data = json.loads(files_json)
                if any(files_data.values()):  # If any values are non-empty
                    content = files_json  # For Anthropic API, send just the JSON
                else:
                    content = prompt
            except json.JSONDecodeError:
                # If it's not valid JSON, combine with prompt
                content = f"{prompt}\n\n{files_json}"
        else:
            content = prompt
        
        # Send to LLM using the same pattern as origin/main processors
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=self.DEFAULT_MAX_TOKENS,
            system=system_prompt or self.get_generic_prompt_template(),
            messages=[{"role": "user", "content": content}]
        )
        
        logger.info(f"LLM usage: {response.usage}")
        
        # Extract and parse the response
        response_text = response.content[0].text
        return self.extract_json_response(response_text)
    
    def extract_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON from the LLM response text.
        
        This follows the exact pattern from origin/main processors.
        """
        try:
            # Look for JSON block in the response (same as origin/main processors)
            json_start = response_text.index("{")
            json_end = response_text.rfind("}")
            json_str = response_text[json_start:json_end + 1]
            return json.loads(json_str)
        except (ValueError, json.JSONDecodeError) as e:
            logger.warning(f"Failed to extract JSON from response: {e}")
            logger.debug(f"Response text: {response_text}")
            # Return empty response if JSON extraction fails
            return {}
    
    def send_fix_request(self, run_logs_files: List[FileReference], 
                        code_files: List[FileReference],
                        memory: List[str],
                        replay_dir: str) -> Dict[str, Any]:
        """
        Send a fix request following the origin/main FixNodeProcessor pattern.
        
        Args:
            run_logs_files: Run log files with content
            code_files: Code files that can be edited
            memory: Memory items from replay state
            replay_dir: Directory containing system instructions
            
        Returns:
            Dict containing the parsed LLM response
        """
        # Build request following origin/main FixNodeProcessor pattern
        request_dict = {
            "prompt": self.get_fix_node_prompt_with_commands(),
            "run_logs_files": [{"path_and_filename": f.path, "contents": f.content} for f in run_logs_files],
            "code_to_edit": [{"path_and_filename": f.path, "contents": f.content} for f in code_files],
            "memory": memory
        }
        
        request_json = json.dumps(request_dict, indent=2)
        
        logger.info(f"⚒️ Sending FIX request to LLM with {len(run_logs_files)} run logs files and {len(code_files)} code files")
        
        # Get system instructions
        system_prompt = self.get_prompt_node_system_instructions(replay_dir)
        
        # Send request
        return self.send_request("", request_json, system_prompt)
    
    def send_prompt_request(self, prompt: str, code_files: List[FileReference],
                          read_only_files: List[FileReference],
                          replay_dir: str) -> Dict[str, Any]:
        """
        Send a prompt request following the origin/main PromptNodeProcessor pattern.
        
        Note: origin/main doesn't include memory in PROMPT requests.
        
        Args:
            prompt: The user prompt
            code_files: Code files that can be edited
            read_only_files: Read-only files (docs, templates, etc.)
            replay_dir: Directory containing system instructions
            
        Returns:
            Dict containing the parsed LLM response
        """
        # Build request following origin/main PromptNodeProcessor pattern (no memory)
        request_dict = {
            "prompt": prompt,
            "code_to_edit": [{"path_and_filename": f.path, "contents": f.content} for f in code_files],
            "read_only_files": [{"path_and_filename": f.path, "contents": f.content} for f in read_only_files]
        }
        
        request_json = json.dumps(request_dict, indent=2)
        
        logger.info(f"📝 Sending PROMPT request to LLM with {len(code_files)} code files and {len(read_only_files)} read-only files")
        
        # Get system instructions
        system_prompt = self.get_prompt_node_system_instructions(replay_dir)
        
        # Send request
        return self.send_request("", request_json, system_prompt)
    
    def get_fix_node_prompt_with_commands(self) -> str:
        """
        Get the fix node prompt with commands support (origin/main pattern).
        
        Returns:
            str: The fix node prompt with commands functionality
        """
        return """
        Review the error logs and suggest fixes for the code files. 
        Don't create new files. Don't make any drastic changes. 
        Carefully review memory, it may contain useful information.
        For wrong includes and api calls, request a "commands_to_run" get_api_reference(<api_name|or_header_name>) to get the correct API reference and examples.
        """
    
    def process_commands_in_response(self, response_data: Dict[str, Any], replay) -> None:
        """
        Process commands_to_run from LLM response (origin/main pattern).
        
        Args:
            response_data: The LLM response data
            replay: The replay instance for updating memory
        """
        if 'commands_to_run' in response_data:
            logger.info(f"Commands to run: {response_data['commands_to_run']}")
            commands_to_run = response_data['commands_to_run']
            for command in commands_to_run:
                if command.startswith('get_api_reference'):
                    api_name = command.split('(')[1].split(')')[0]
                    api_reference = self._get_mock_api_reference(api_name)
                    replay.state.execution.memory.append(f"A call to get_api_reference({api_name}) was requested. It returned: {api_reference}")                    
                    logger.info(f"✨✨✨ Tool is used. Added a reference to memory: {api_reference}")
    
    def _get_mock_api_reference(self, api_name: str) -> str:
        """Get the API reference for a given API name (origin/main pattern)."""
        return """
## Wrong header usage
If you get an error like "No such file or directory" for an include - remove this include.

## no match for 'operator/'
// Instead of: result = (1.0f / val) * other_val;
sfpi::vFloat result = ckernel::sfpu::_sfpu_reciprocal_(val) * other_val;

// Or for constants:
sfpi::vFloat one = sfpi::vFloat(1.0f);  // Convert to vFloat first
"""