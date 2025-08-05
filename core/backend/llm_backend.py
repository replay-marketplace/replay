from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import os


class LLMBackend(ABC):
    """
    Abstract base class for backend LLM implementations.
    
    This class provides the interface that all LLM backend implementations
    should follow. It includes methods for getting model information,
    packaging files for requests, and providing various prompts used
    by different node processors.
    """
    
    def __init__(self, model_name: str):
        """
        Initialize the LLM backend with a model name.
        
        Args:
            model_name (str): The name of the model to use
        """
        self.model_name = model_name
    
    def get_model_name(self) -> str:
        """
        Get the model name for this backend.
        
        Returns:
            str: The model name
        """
        return self.model_name
    
    def package_files(self, file_paths: List[str]) -> str:
        """
        Package a list of files for an LLM request.
        
        This method takes a list of file paths and returns a JSON representation
        of those files suitable for sending to an LLM. The JSON format includes
        both the file paths and their contents.
        
        Args:
            file_paths (List[str]): List of file paths to package
            
        Returns:
            str: JSON string representing the files
        """
        files_data = []
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    files_data.append({
                        "path_and_filename": file_path,
                        "contents": content
                    })
                except Exception as e:
                    # If we can't read a file, include it with an error message
                    files_data.append({
                        "path_and_filename": file_path,
                        "contents": f"Error reading file: {str(e)}"
                    })
            else:
                # If file doesn't exist, include it with a not found message
                files_data.append({
                    "path_and_filename": file_path,
                    "contents": "File not found"
                })
        
        return json.dumps(files_data, indent=2)
    
    # Prompt methods matching processor patterns
    
    def get_fix_node_prompt(self) -> str:
        """
        Get the prompt used by FixNodeProcessor.
        
        Returns:
            str: The fix node prompt
        """
        return """
        Review the error logs and suggest fixes for the code files. 
        Don't create new files. Don't make any drastic changes. 
        Carefully review memory, it may contain useful information.
        """
    
    def get_prompt_node_system_instructions(self, replay_dir: str) -> str:
        """
        Get the system instructions used by PromptNodeProcessor.
        
        Args:
            replay_dir (str): The replay directory containing instructions
            
        Returns:
            str: The system instructions content
        """
        instructions_file = self.CLIENT_INSTRUCTIONS_FILE
        instructions_path = os.path.join(replay_dir, instructions_file)
        
        if os.path.exists(instructions_path):
            try:
                with open(instructions_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                raise Exception(f"Error reading client instructions from {instructions_path}: {e}")
        else:
            raise FileNotFoundError(f"Client instructions file not found: {instructions_path}")
    
    def get_generic_prompt_template(self) -> str:
        """
        Get a generic prompt template for basic LLM requests.
        
        Returns:
            str: A generic prompt template
        """
        return """
        Please analyze the provided files and respond according to the given prompt.
        Provide your response in JSON format with the following structure:
        {
            "files": [
                {
                    "path_and_filename": "path/to/file.ext",
                    "contents": "file contents here"
                }
            ],
            "memory": ["memory item 1", "memory item 2"]
        }
        """
    
    def send_fix_request(self, run_logs_files: List, code_files: List, 
                        read_only_files: List = None, memory: List[str] = None, 
                        replay_dir: str = None) -> Dict[str, Any]:
        """
        Send a fix request to the LLM backend.
        
        This is a common implementation that handles the basic structure.
        Subclasses can override for backend-specific behavior.
        
        Args:
            run_logs_files: Run log files with content
            code_files: Code files that can be edited
            read_only_files: List of read-only files (optional)
            memory: Memory items from replay state (optional)
            replay_dir: Directory containing system instructions (optional)
            
        Returns:
            Dict containing the parsed LLM response
        """
        # For anthropic_api backend, read_only_files should be empty
        if read_only_files is None:
            read_only_files = []
        
        # Build request with the fix prompt
        prompt = self.get_fix_node_prompt()
        
        # Package files for request - subclasses will handle this differently
        files_json = self.package_files(
            [f.path for f in code_files + run_logs_files] + read_only_files
        )
        
        # Get system instructions
        system_prompt = None
        if replay_dir:
            system_prompt = self.get_prompt_node_system_instructions(replay_dir)
        
        # Send request
        return self.send_request(prompt, files_json, system_prompt)
    
    # Abstract methods that concrete implementations must provide
    
    @abstractmethod
    def send_request(self, prompt: str, files_json: str, system_prompt: str = None) -> Dict[str, Any]:
        """
        Send a request to the LLM backend.
        
        Args:
            prompt (str): The user prompt
            files_json (str): JSON string containing files data
            system_prompt (str, optional): System prompt/instructions
            
        Returns:
            Dict[str, Any]: The parsed response from the LLM
        """
        pass
    
    @abstractmethod
    def extract_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON from the LLM response text.
        
        Args:
            response_text (str): The raw response text from the LLM
            
        Returns:
            Dict[str, Any]: The parsed JSON response
        """
        pass