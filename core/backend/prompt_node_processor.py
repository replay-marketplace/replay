import json
import logging
import os
from typing import Dict, List, Any
from dataclasses import dataclass

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

class PromptNodeProcessor:
    """Processes PROMPT nodes by sending prompts to LLM and handling responses."""
    
    # Configuration constants
    #DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
    DEFAULT_MODEL = "claude-3-7-sonnet-20250219"
    DEFAULT_MAX_TOKENS = 10000
    CLIENT_INSTRUCTIONS_FILE = "client_instructions_with_json.txt"
    
    def process_generic_prompt(self, replay, node):
        """Process a generic prompt."""
        # Extract node data and build request
        node_data = self._extract_node_data_for_generic_prompt(replay, node)
        llm_request = self._build_generic_llm_request(node_data, replay)
        
        # Send request to LLM
        response_data = self._send_generic_llm_request(replay, node_data, llm_request)
        
        # Process and save response
        self._process_generic_llm_response(response_data, replay)

    def process_investigation_prompt(self, replay, node):
        """Process an investigation prompt."""
        node_data = self._extract_node_data_for_investigation_prompt(replay, node)
        llm_request = self._build_investigation_llm_request(node_data, replay)
        response_data = self._send_investigation_llm_request(replay, node_data, llm_request)
        data = self._process_investigation_llm_response(response_data, replay)
        node_content = node.get('contents', {})
        node_content['response'] = data
        logger.info(f"Investigation prompt response: \n{json.dumps(data, indent=2)}")

    def _extract_node_data_for_investigation_prompt(self, replay, node: dict) -> Dict[str, Any]:
        """Extract data from the node."""
        contents = node.get('contents', {})
        
        return {
            'type': contents.get('type', None),
            'prompt': contents.get('prompt', ''),
            'run_logs_refs': contents.get('run_logs_refs', [])
        }

    def _build_investigation_llm_request(self, node_data: Dict[str, Any], replay) -> LLMRequest:
        """Build the LLM request from node data."""
        prompt_content = node_data['prompt']
        run_logs_files = self._load_files_from_directory(node_data['run_logs_refs'], replay.run_logs_dir, "run logs file")
        
        return LLMRequest(
            prompt=prompt_content,
            run_logs_files=run_logs_files
        )
    
    def _send_investigation_llm_request(self, replay, node_data: Dict[str, Any], llm_request: LLMRequest) -> Dict[str, Any]:
        """Send the LLM request and return the parsed response."""
        # Convert to JSON format expected by LLM
        request_dict = {
            "prompt": llm_request.prompt,
            "run_logs_files": [{"path_and_filename": f.path, "contents": f.content} for f in llm_request.run_logs_files]
        }        
        request_json = json.dumps(request_dict, indent=2)
        
        logger.info(
            f"Sending request to LLM with {len(llm_request.run_logs_files)} run logs files"
        )
        
        # Get client instructions
        system_prompt = self._get_client_instructions(replay.replay_dir, "investigation")
        
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
    # {
    # "path": "file1.cpp", 
    # "line_number": 5,
    # "reason": "Includes a file <path> that can't be found",
    # "fix": "Add the file to the project"
    # }
    def _process_investigation_llm_response(self, response_data: Dict[str, Any], replay) -> None:
        """Process the LLM response and save generated files."""
        return {
            'path_to_fix': response_data['path'],
            'line_number': response_data['line_number'],
            'reason': response_data['reason'],
            'fix': response_data['fix']
        }           

    def process(self, replay, node: dict) -> None:
        """
        Process a PROMPT node by sending the prompt to the LLM and saving the response.
        
        Args:
            replay: The replay instance containing state and client
            node: The node data dictionary to process
        """
        processors = {
            "generic": self.process_generic_prompt,
            "investigation": self.process_investigation_prompt,
            #"fix": self.process_fix_prompt
        }
        
        try:
            type = node.get('contents', {}).get('type', "generic")
            logger.info(f"Processing PROMPT node {node} with type {type}")
            processor = processors[type]
            processor(replay, node)
            
            logger.info(f"Successfully processed PROMPT node {node}")
            
        except Exception as e:
            logger.error(f"Error processing PROMPT node {node}: {e}")
            raise

    def _extract_node_data_for_generic_prompt(self, replay, node: dict) -> Dict[str, Any]:
        """Extract data from the node."""
        contents = node.get('contents', {})
        
        return {
            'type': contents.get('type', None),
            'prompt': contents.get('prompt', ''),
            'code_refs': contents.get('code_refs', []),
            'docs_refs': contents.get('docs_refs', []),
            'template_refs': contents.get('template_refs', []),
            'run_logs_refs': contents.get('run_logs_refs', [])
        }

    def _build_generic_llm_request(self, node_data: Dict[str, Any], replay) -> LLMRequest:
        """Build the LLM request from node data."""
        prompt_content = node_data['prompt']
        code_files = self._load_code_files(node_data['code_refs'], replay.code_dir)
        read_only_files = self._load_read_only_files(
            node_data['docs_refs'], 
            node_data['template_refs'], 
            node_data['run_logs_refs'],
            replay.replay_dir
        )
        
        return LLMRequest(
            prompt=prompt_content,
            code_to_edit=code_files,
            read_only_files=read_only_files
        )

    def _load_code_files(self, code_refs: List[str], code_dir: str) -> List[FileReference]:
        """Load code files that can be edited."""
        return self._load_files_from_directory(code_refs, code_dir, "code file")

    def _load_read_only_files(self, docs_refs: List[str], template_refs: List[str], run_logs_refs: List[str], base_dir: str) -> List[FileReference]:
        """Load read-only files (docs and templates)."""
        all_files = []
        
        # Load docs files from the docs subdirectory
        docs_dir = os.path.join(base_dir, "docs")
        docs_files = self._load_files_from_directory(docs_refs, docs_dir, "docs file")
        all_files.extend(docs_files)
        
        # Load template files from the template subdirectory
        template_dir = os.path.join(base_dir, "template")
        template_files = self._load_files_from_directory(template_refs, template_dir, "template file")
        all_files.extend(template_files)
        
        # Load run logs files from the run_logs subdirectory
        run_logs_dir = os.path.join(base_dir, "run_logs")
        run_logs_files = self._load_files_from_directory(run_logs_refs, run_logs_dir, "run logs file", last_n_lines=100)
        all_files.extend(run_logs_files)
        
        return all_files

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

    def _read_file_safely(self, file_path: str, last_n_lines: int = None) -> str:
        """Read a file safely with proper encoding handling."""        
        with open(file_path, 'r', encoding='utf-8') as f:
            if last_n_lines is not None:
                return '\n'.join(f.readlines()[-last_n_lines:])
            else:
                return f.read()
            
    def _get_client_instructions(self, replay_dir: str, prompt_type: str) -> str:
        """Load client instructions from the replay directory."""
        prompts = {
            None: self.CLIENT_INSTRUCTIONS_FILE,
            "investigation": "client_instructions_indentify_issue.txt"
        }
        
        file = self.CLIENT_INSTRUCTIONS_FILE
        if prompt_type is not None:
            file = prompts[prompt_type]

        instructions_path = os.path.join(replay_dir, file)
        
        if os.path.exists(instructions_path):
            try:
                return self._read_file_safely(instructions_path)
            except Exception as e:
                raise Exception(f"Error reading client instructions for type {prompt_type} from {instructions_path}: {e}")
        else:
            raise FileNotFoundError(f"Client instructions file not found for type {prompt_type}: {instructions_path}")

    def _send_generic_llm_request(self, replay, node_data: Dict[str, Any], llm_request: LLMRequest) -> Dict[str, Any]:
        """Send the LLM request and return the parsed response."""
        # Convert to JSON format expected by LLM
        request_dict = {
            "prompt": llm_request.prompt,
            "code_to_edit": [{"path_and_filename": f.path, "contents": f.content} for f in llm_request.code_to_edit],
            "read_only_files": [{"path_and_filename": f.path, "contents": f.content} for f in llm_request.read_only_files]
        }
        
        request_json = json.dumps(request_dict, indent=2)
        
        logger.info(
            f"Sending request to LLM with {len(llm_request.code_to_edit)} code files "
            f"and {len(llm_request.read_only_files)} read-only files"
        )
        
        # Get client instructions

        system_prompt = self._get_client_instructions(replay.replay_dir, node_data['type'])
        
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

    def _save_generated_file(self, file_path: str, content: str, code_dir: str) -> None:
        """Save a generated file to the code directory."""
        full_path = os.path.join(code_dir, file_path)
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Write file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Saved generated file: {full_path}")
            
        except Exception as e:
            logger.error(f"Error saving generated file {full_path}: {e}")
            raise 