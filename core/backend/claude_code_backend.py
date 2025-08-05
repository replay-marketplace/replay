import json
import logging
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .llm_backend import LLMBackend
from .claude_code_config import ClaudeCodeConfig

logger = logging.getLogger(__name__)


@dataclass
class FileReference:
    """Represents a file reference with path and content."""
    path: str
    content: str


class ClaudeCodeBackend(LLMBackend):
    """
    Claude Code backend implementation that uses the configured Claude Code client.
    
    This implementation follows the patterns established in the existing processors,
    particularly how they package files and send requests to the LLM.
    """
    
    DEFAULT_MAX_TOKENS = 10000
    CLIENT_INSTRUCTIONS_FILE = "client_instructions_with_json_claude.txt"
    
    def __init__(self, client=None):
        """
        Initialize the Claude Code backend.
        
        Args:
            client: Optional pre-configured client. If None, will be provided by replay context.
        """
        # Load configuration to get the model name
        config = ClaudeCodeConfig()
        
        # Get model name from settings.json, fallback to environment, then default
        model_name = config.settings.get("model")
        if not model_name:
            model_name = os.environ.get("ANTHROPIC_MODEL", "anthropic/claude-sonnet-4-20250514")
        
        super().__init__(model_name)
        
        self.config = config
        self.client = client  # Will be set by replay context
        
        logger.info(f"Initialized ClaudeCodeBackend with model: {self.model_name}")
        # Log configuration status only when using Claude Code backend
        config.log_configuration_status()
    
    def package_files_for_request(self, code_files: List[FileReference], 
                                read_only_files: List[FileReference],
                                run_logs_files: List[FileReference] = None,
                                memory: List[str] = None) -> Dict[str, Any]:
        """
        Package files for an LLM request in the format expected by processors.
        
        This method follows the pattern used in PromptNodeProcessor and FixNodeProcessor
        where files are packaged as just the file paths, not the full contents.
        
        Args:
            code_files: Files that can be edited
            read_only_files: Files that are read-only (docs, templates, etc.)
            run_logs_files: Run log files (optional)
            memory: Memory items (optional)
            
        Returns:
            Dict containing the packaged request data
        """
        request_data = {
            "code_to_edit": [f.path for f in code_files],
            "read_only_files": [f.path for f in read_only_files],
        }
        
        if run_logs_files:
            request_data["run_logs_files"] = [f.path for f in run_logs_files]
            
        if memory:
            request_data["memory"] = memory
            
        return request_data
    
    def load_files_from_directory(self, file_refs: List[str], base_dir: str, 
                                file_type: str, last_n_lines: int = None) -> List[FileReference]:
        """
        Load files from a directory and return FileReference objects.
        
        This follows the exact pattern from the processors.
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
        Send a request to the Claude Code LLM.
        
        This follows the pattern established in the processors where the client
        is accessed from the replay context.
        
        Args:
            prompt: The user prompt
            files_json: JSON string containing the request data
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
                    content = f"{prompt}\n\n{files_json}"
                else:
                    content = prompt
            except json.JSONDecodeError:
                # If it's not valid JSON, just append it
                content = f"{prompt}\n\n{files_json}"
        else:
            content = prompt
        
        # Send to LLM using the same pattern as processors
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
        
        This follows the pattern from the processors which look for JSON blocks
        in the response.
        """
        try:
            # Look for JSON block in the response (same as processors)
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
                        read_only_files: List[str] = None,
                        memory: List[str] = None,
                        replay_dir: str = None) -> Dict[str, Any]:
        """
        Send a fix request following the Claude Code pattern.
        
        Args:
            run_logs_files: Run log files with content
            code_files: Code files that can be edited
            read_only_files: List of read-only file paths
            memory: Memory items from replay state
            replay_dir: Directory containing system instructions
            
        Returns:
            Dict containing the parsed LLM response
        """
        # Ensure defaults are set
        if read_only_files is None:
            read_only_files = []
        if memory is None:
            memory = []
        
        # Override super() implementation to use file paths only for claude_code
        # Build request following FixNodeProcessor pattern with paths only
        request_dict = {
            "prompt": self.get_fix_node_prompt(),
            "run_logs_files": [f.path for f in run_logs_files],
            "code_to_edit": [f.path for f in code_files],
            "read_only_files": read_only_files,
            "memory": memory
        }
        
        request_json = json.dumps(request_dict, indent=2)
        
        logger.info(f"⚒️ Sending FIX request to LLM with {len(run_logs_files)} run logs files and {len(code_files)} code files")
        
        # Get system instructions
        system_prompt = None
        if replay_dir:
            system_prompt = self.get_prompt_node_system_instructions(replay_dir)
        
        # Send request
        return self.send_request("", request_json, system_prompt)
    
    def send_prompt_request(self, prompt: str, code_files: List[FileReference],
                          read_only_files: List[FileReference],
                          memory: List[str],
                          replay_dir: str) -> Dict[str, Any]:
        """
        Send a prompt request following the PromptNodeProcessor pattern.
        
        Args:
            prompt: The user prompt
            code_files: Code files that can be edited
            read_only_files: Read-only files (docs, templates, etc.)
            memory: Memory items from replay state
            replay_dir: Directory containing system instructions
            
        Returns:
            Dict containing the parsed LLM response
        """
        # Build request following PromptNodeProcessor pattern
        request_dict = {
            "prompt": prompt,
            "code_to_edit": [f.path for f in code_files],
            "read_only_files": [f.path for f in read_only_files],
            "memory": memory
        }
        
        request_json = json.dumps(request_dict, indent=2)
        
        logger.info(f"📝 Sending PROMPT request to LLM with {len(code_files)} code files and {len(read_only_files)} read-only files")
        
        # Get system instructions
        system_prompt = self.get_prompt_node_system_instructions(replay_dir)
        
        # Send request
        return self.send_request("", request_json, system_prompt)