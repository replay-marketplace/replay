import json
import logging
import os
import xml.etree.ElementTree as ET
from typing import Dict, List, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class FileReference:
    """Represents a file reference with path, content, and line numbers."""
    path: str
    content: str
    line_numbers: bool = True

@dataclass
class LLMRequest:
    """Represents an LLM request with prompt and file references."""
    prompt: str
    code_to_edit: List[FileReference]
    read_only_files: List[FileReference]
    run_logs_files: List[FileReference]
    memory: List[str]

class PromptNodeProcessorXML:
    """Processes PROMPT nodes using XML format for better LLM interaction."""
    
    # Configuration constants
    DEFAULT_MODEL = "claude-3-7-sonnet-20250219"
    DEFAULT_MAX_TOKENS = 10000
    CLIENT_INSTRUCTIONS_FILE = "client_instructions_with_xml.txt"
    
    def process_generic_prompt(self, replay, node):
        """Process a generic prompt using XML format."""
        # Extract node data and build request
        node_data = self._extract_node_data_for_generic_prompt(replay, node)
        llm_request = self._build_generic_llm_request(node_data, replay)
        
        # Send request to LLM
        response_data = self._send_generic_llm_request(replay, node_data, llm_request)
        
        # Process and save response
        self._process_generic_llm_response(response_data, replay)

    def process(self, replay, node: dict) -> None:
        """
        Process a PROMPT node by sending the prompt to the LLM and saving the response.
        
        Args:
            replay: The replay instance containing state and client
            node: The node data dictionary to process
        """
        try:
            logger.info(f"Processing PROMPT node {node}")
            
            # For now, all PROMPT nodes are treated as generic
            self.process_generic_prompt(replay, node)
            
            logger.info(f"Successfully processed PROMPT node {node}")
            
        except Exception as e:
            logger.error(f"Error processing PROMPT node {node}: {e}")
            raise

    def _extract_node_data_for_generic_prompt(self, replay, node: dict) -> Dict[str, Any]:
        """Extract data from the node."""
        contents = node.get('contents', {})
        
        return {
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
            read_only_files=read_only_files,
            run_logs_files=[], # not used here
            memory=replay.state.execution.memory
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
        """Read a file safely with proper encoding handling and line numbers."""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            if last_n_lines is not None:
                lines = lines[-last_n_lines:]
            
            # Add line numbers to content
            numbered_content = []
            start_line = len(lines) - len(lines) + 1 if last_n_lines else 1
            
            for i, line in enumerate(lines, start=start_line):
                numbered_content.append(f"{i:4d}: {line.rstrip()}")
            
            return '\n'.join(numbered_content)
            
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

    def _build_xml_request(self, llm_request: LLMRequest) -> str:
        """Build XML format request for LLM using semantic tags."""
        xml_parts = []
        
        # Add code files to edit (no readonly attribute)
        if llm_request.code_to_edit:
            for file_ref in llm_request.code_to_edit:
                xml_parts.append(f'<file path="{file_ref.path}">')
                xml_parts.append(self._escape_xml(file_ref.content))
                xml_parts.append('</file>')
        
        # Add read-only files (with readonly flag)
        if llm_request.read_only_files:
            for file_ref in llm_request.read_only_files:
                xml_parts.append(f'<file path="{file_ref.path}" readonly>')
                xml_parts.append(self._escape_xml(file_ref.content))
                xml_parts.append('</file>')
        
        # Add memory
        if llm_request.memory:
            xml_parts.append('<memory>')
            for entry in llm_request.memory:
                xml_parts.append(f'<entry>{self._escape_xml(entry)}</entry>')
            xml_parts.append('</memory>')
        
        return '\n'.join(xml_parts)

    def _escape_xml(self, text: str) -> str:
        """Escape XML special characters."""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

    def _send_generic_llm_request(self, replay, node_data: Dict[str, Any], llm_request: LLMRequest) -> Dict[str, Any]:
        """Send the LLM request and return the parsed response."""
        # Build XML request
        xml_request = self._build_xml_request(llm_request)
        
        # Combine prompt with XML content
        full_request = f"{llm_request.prompt}\n\n{xml_request}"
        
        logger.info(
            f"Sent XML request to LLM with {len(llm_request.code_to_edit)} code files "
            f"and {len(llm_request.read_only_files)} read-only files"
        )
        
        # Get client instructions
        system_prompt = self._get_client_instructions(replay.replay_dir)
        
        # Send to LLM
        response = replay.client.messages.create(
            model=self.DEFAULT_MODEL,
            max_tokens=self.DEFAULT_MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": full_request}]
        )
        
        # Parse XML response
        response_content = response.content[0].text
        return self._parse_xml_response(response_content)

    def _parse_xml_response(self, response_content: str) -> Dict[str, Any]:
        """Parse XML response from LLM."""
        try:
            # Try to find XML content - look for common root elements
            xml_start = -1
            xml_end = -1
            
            # Look for common root elements
            for root_tag in ['<file', '<edit', '<commands', '<memory']:
                start_pos = response_content.find(root_tag)
                if start_pos != -1:
                    xml_start = start_pos
                    break
            
            if xml_start == -1:
                raise ValueError("No XML content found")
            
            # Find the end by looking for the last closing tag
            for root_tag in ['</file>', '</edit>', '</commands>', '</memory>']:
                end_pos = response_content.rfind(root_tag)
                if end_pos != -1:
                    xml_end = end_pos + len(root_tag)
            
            if xml_end == -1:
                raise ValueError("No closing XML tags found")
            
            xml_content = response_content[xml_start:xml_end]
            
            # Wrap in a temporary root for parsing
            wrapped_xml = f"<root>{xml_content}</root>"
            root = ET.fromstring(wrapped_xml)
            
            result = {
                'files': [],
                'commands': [],
                'memory': []
            }
            
            # Parse file and edit elements
            for file_elem in root.findall('file'):
                result['files'].append({
                    'path_and_filename': file_elem.get('path'),
                    'contents': file_elem.text if file_elem.text else ''
                })
            
            for edit_elem in root.findall('edit'):
                # Handle edits - convert to new file content
                # Check for line or lines attributes
                line_attr = edit_elem.get('line')
                lines_attr = edit_elem.get('lines')
                
                result['files'].append({
                    'path_and_filename': edit_elem.get('file'),
                    'contents': edit_elem.text if edit_elem.text else '',
                    'line': line_attr,
                    'lines': lines_attr
                })
            
            # Parse commands
            commands_elem = root.find('commands')
            if commands_elem is not None:
                for cmd_elem in commands_elem.findall('command'):
                    result['commands'].append(cmd_elem.text)
            
            # Parse memory
            memory_elem = root.find('memory')
            if memory_elem is not None:
                for entry_elem in memory_elem.findall('entry'):
                    result['memory'].append(entry_elem.text)
            
            return result
            
        except ET.ParseError as e:
            logger.error(f"Failed to parse XML response: {e}")
            logger.error(f"Response content: {response_content}")
            raise
        except Exception as e:
            logger.error(f"Error parsing XML response: {e}")
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
            
            logger.info(f"Saved generated file: {full_path}")
            
        except Exception as e:
            logger.error(f"Error saving generated file {full_path}: {e}")
            raise 