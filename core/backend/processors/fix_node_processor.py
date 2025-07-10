import json
import logging
import os
import re
from typing import Dict, List, Any, Union
from dataclasses import dataclass
from core.prompt_preprocess2.ir.ir import Opcode
from .base_processor import BaseProcessor, FileReference

logger = logging.getLogger(__name__)

@dataclass
class LLMRequest:
    """Represents an LLM request with prompt and file references."""
    prompt: str
    code_to_edit: List[FileReference]
    read_only_files: List[FileReference]
    run_logs_files: List[FileReference]
    memory: List[str]

class FixNodeProcessor(BaseProcessor):
    """Processes FIX nodes by analyzing run logs and applying fixes to code using XML and tool use."""
    
    # Configuration constants
    DEFAULT_MODEL = "claude-3-7-sonnet-20250219"
    DEFAULT_MAX_TOKENS = 10000
    LAST_N_ERROR_LINES = 100
    CLIENT_INSTRUCTIONS_FILE = "client_instructions_with_xml.txt"
    MAX_CONVERSATION_TOKENS = 100000  # Conservative limit for context window
    TOKEN_ESTIMATION_RATIO = 4  # Characters per token (rough estimation)
    
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
            stderr_file_content = self._load_files_from_directory([stdout_file], replay.run_logs_dir, "run log file", last_n_lines=self.LAST_N_ERROR_LINES)
            run_logs_files = self._load_files_from_directory([stderr_file], replay.run_logs_dir, "stderr file", last_n_lines=self.LAST_N_ERROR_LINES)
            logger.debug(f"Found attached run logs files: {run_logs_files}")

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
            
            # Process response using tool use and XML parsing
            original_request = f"{llm_request.prompt}\n\n{self._build_xml_request(llm_request)}"
            self._process_llm_response(response_data, replay, original_request)
            
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
        all: bool = False  # Changed from True to False to actually filter files

        code_dir = replay.code_dir
        run_logs_dir = replay.run_logs_dir
        code_files = []        

        if os.path.exists(code_dir):
            logger.debug(f"Found code files in {code_dir}")
            for file_name in os.listdir(code_dir):
                logger.debug(f"Found code file: {file_name}")
                if os.path.isfile(os.path.join(code_dir, file_name)):
                    logger.debug(f"Its a file: {file_name}")
                    code_files.append(file_name)

        code_files = [f for f in code_files if not f.startswith('.')] # exclude files/folders starting with .
        if all:
            return code_files

        relevant_code_files = []
        log_content = self.read_file_safely(os.path.join(run_logs_dir, log_file), last_n_lines=self.LAST_N_ERROR_LINES)
        logger.info(f"Log content: {log_content}")
        for file_name in code_files:
            logger.debug(f"Checking if {file_name} is in log content")
            if file_name in log_content:
                logger.debug(f"Found {file_name} in log content")
                relevant_code_files.append(file_name)
            else:
                logger.debug(f"Did not find {file_name} in log content")
        
        return relevant_code_files

    def _load_files_from_directory(self, file_refs: List[str], base_dir: str, file_type: str, last_n_lines: int = None) -> List[FileReference]:
        """Load files from a directory and return FileReference objects."""
        files = []
        
        for file_ref in file_refs:
            file_path = os.path.join(base_dir, file_ref)
            
            if os.path.exists(file_path):
                try:
                    content = self.read_file_safely(file_path, last_n_lines)
                    files.append(FileReference(path=file_ref, content=content))
                    logger.info(f"Added {file_type} file: {file_ref}")
                except Exception as e:
                    logger.error(f"Error reading {file_type} {file_path}: {e}")
            else:
                logger.warning(f"{file_type.title()} not found: {file_path}")
        
        return files

    def _build_llm_request(self, run_logs_files: List[FileReference], code_files: List[FileReference], replay) -> LLMRequest:
        """Build the LLM request for analysis."""
        prompt = """
        Review the error logs and suggest fixes for the code files. 
        Don't create new files. Don't make any drastic changes. 
        Carefully review memory, it may contain useful information.
        For wrong includes and api calls, use the get_api_reference tool to get the correct API reference and examples.
        """
        
        return LLMRequest(
            prompt=prompt,
            code_to_edit=code_files,
            read_only_files=run_logs_files, # run logs are read-only
            run_logs_files=run_logs_files,
            memory=replay.state.execution.memory # use memory from replay state
        )

    def _build_xml_request(self, llm_request: LLMRequest) -> str:
        """Build XML format request for LLM using semantic tags."""
        xml_parts = []
        
        # Add code files to edit (no readonly attribute)
        if llm_request.code_to_edit:
            for file_ref in llm_request.code_to_edit:
                xml_parts.append(f'<file path="{file_ref.path}">')
                xml_parts.append(self.escape_xml(file_ref.content))
                xml_parts.append('</file>')
        
        # Add read-only files (with readonly flag)
        if llm_request.read_only_files:
            for file_ref in llm_request.read_only_files:
                xml_parts.append(f'<file path="{file_ref.path}" readonly>')
                xml_parts.append(self.escape_xml(file_ref.content))
                xml_parts.append('</file>')
        
        # Add memory
        if llm_request.memory:
            xml_parts.append('<memory>')
            for entry in llm_request.memory:
                xml_parts.append(f'<entry>{self.escape_xml(entry)}</entry>')
            xml_parts.append('</memory>')
        
        return '\n'.join(xml_parts)

    def _send_llm_request(self, replay, llm_request: LLMRequest) -> Union[str, Dict[str, Any]]:
        """Send the LLM request and return the response."""
        # Build XML request
        xml_request = self._build_xml_request(llm_request)
        
        # Combine prompt with XML content
        full_request = f"{llm_request.prompt}\n\n{xml_request}"
        
        logger.info(f"⚒️ Sending FIX request to LLM with {len(llm_request.run_logs_files)} run logs files and {len(llm_request.code_to_edit)} code files")
        
        # Get client instructions
        system_prompt = self._get_client_instructions(replay.replay_dir)
        
        # Get available tools for Anthropic with proper schema format
        tools = self.get_anthropic_tools_schema()
        
        # Send to LLM with tools enabled
        response = replay.client.messages.create(
            model=self.DEFAULT_MODEL,
            max_tokens=self.DEFAULT_MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": full_request}],
            tools=tools
        )
        logger.info(f"LLM usage: {response.usage}")
        
        return response

    def _process_llm_response(self, response, replay, original_request=None) -> None:
        """Process the LLM response using proper Anthropic tool use handling."""
        # Check if response contains tool use
        if response.stop_reason == "tool_use":
            # Build initial conversation history from the original request
            conversation_history = self._build_initial_conversation_history(original_request) if original_request else []
            # Handle tool use according to Anthropic specification
            self._handle_tool_use_response(response, replay, conversation_history)
        else:
            # Handle regular response - just log it and store in memory
            response_content = response.content[0].text if response.content else ""
            logger.info(f"Received non-tool response. Content length: {len(response_content)}")
            
            if response_content.strip():
                # Store the response in memory for future reference
                self.store_in_memory(replay, "fix_processor_response", f"LLM response: {response_content[:500]}...")
                logger.info(f"LLM response: {response_content}")
            else:
                logger.info("Empty response received")

    def _build_initial_conversation_history(self, original_request: str) -> List[Dict[str, Any]]:
        """Build the initial conversation history from the original request."""
        return [{"role": "user", "content": original_request}]

    def _handle_tool_use_response(self, response, replay, conversation_history=None) -> None:
        """Handle tool use response according to Anthropic specification."""
        tool_results = self.handle_tool_use_response(response, replay, conversation_history)
        
        # Continue conversation with tool results
        if tool_results:
            self._continue_with_tool_results(response, tool_results, replay, conversation_history)

    def _continue_with_tool_results(self, original_response, tool_results, replay, conversation_history=None) -> None:
        """Continue the conversation with tool results, managing conversation history and token limits."""
        # Initialize conversation history if not provided
        if conversation_history is None:
            conversation_history = []
        
        # Add the tool use response and results to conversation history
        conversation_history.extend([
            {"role": "assistant", "content": original_response.content},
            {"role": "user", "content": tool_results}  # All results in single message
        ])
        
        # Check if we're approaching token limits (rough estimation)
        estimated_tokens = self._estimate_conversation_tokens(conversation_history)
        
        if estimated_tokens > self.MAX_CONVERSATION_TOKENS:
            logger.warning(f"Conversation approaching token limit ({estimated_tokens} tokens). Truncating history.")
            # Keep only the most recent messages while preserving essential context
            conversation_history = self._truncate_conversation_history(conversation_history, self.MAX_CONVERSATION_TOKENS // 2)
        
        # Get available tools
        tools = self.get_anthropic_tools_schema()
        
        # Continue conversation
        try:
            continuation_response = replay.client.messages.create(
                model=self.DEFAULT_MODEL,
                max_tokens=self.DEFAULT_MAX_TOKENS,
                messages=conversation_history,
                tools=tools
            )
            
            # Process the final response
            if continuation_response.stop_reason == "tool_use":
                # Handle additional tool use if needed, passing conversation history
                self._handle_tool_use_response(continuation_response, replay, conversation_history)
            else:
                # Handle regular continuation response - just log it and store in memory
                response_content = continuation_response.content[0].text if continuation_response.content else ""
                logger.info(f"Received continuation response. Content length: {len(response_content)}")
                
                if response_content.strip():
                    # Store the response in memory for future reference
                    self.store_in_memory(replay, "fix_processor_continuation", f"Continuation response: {response_content[:500]}...")
                    logger.info(f"Continuation response: {response_content}")
                else:
                    logger.info("Empty continuation response received")
        except Exception as e:
            logger.error(f"Error during conversation continuation: {e}")
            # Store error in memory for debugging
            self.store_in_memory(replay, "fix_processor_error", f"Conversation continuation error: {str(e)}")

    def _estimate_conversation_tokens(self, messages: List[Dict[str, Any]]) -> int:
        """Roughly estimate the number of tokens in the conversation."""
        total_tokens = 0
        for message in messages:
            if isinstance(message.get('content'), str):
                # Rough estimation: 1 token ≈ 4 characters
                total_tokens += len(message['content']) // self.TOKEN_ESTIMATION_RATIO
            elif isinstance(message.get('content'), list):
                for content_block in message['content']:
                    if hasattr(content_block, 'text'):
                        total_tokens += len(content_block.text) // self.TOKEN_ESTIMATION_RATIO
                    elif isinstance(content_block, dict) and 'text' in content_block:
                        total_tokens += len(content_block['text']) // self.TOKEN_ESTIMATION_RATIO
                    elif isinstance(content_block, dict) and 'input' in content_block:
                        # Handle tool use blocks
                        input_str = str(content_block['input'])
                        total_tokens += len(input_str) // self.TOKEN_ESTIMATION_RATIO
        return total_tokens

    def _truncate_conversation_history(self, messages: List[Dict[str, Any]], target_tokens: int) -> List[Dict[str, Any]]:
        """Truncate conversation history while preserving essential context."""
        if len(messages) <= 2:
            return messages  # Keep at least the last exchange
        
        # Keep the first message (original context) and the most recent messages
        kept_messages = [messages[0]]  # Original context
        
        # Add recent messages from the end, staying within token limit
        current_tokens = self._estimate_conversation_tokens(kept_messages)
        
        for message in reversed(messages[1:]):
            message_tokens = self._estimate_conversation_tokens([message])
            if current_tokens + message_tokens <= target_tokens:
                kept_messages.append(message)
                current_tokens += message_tokens
            else:
                break
        
        # Reverse back to chronological order
        kept_messages.reverse()
        
        logger.info(f"Truncated conversation from {len(messages)} to {len(kept_messages)} messages")
        return kept_messages

    def _get_client_instructions(self, replay_dir: str) -> str:
        """Load client instructions from the replay directory."""
        instructions_path = os.path.join(replay_dir, self.CLIENT_INSTRUCTIONS_FILE)
        
        if os.path.exists(instructions_path):
            try:
                return self.read_file_safely(instructions_path)
            except Exception as e:
                raise Exception(f"Error reading client instructions from {instructions_path}: {e}")
        else:
            raise FileNotFoundError(f"Client instructions file not found: {instructions_path}") 