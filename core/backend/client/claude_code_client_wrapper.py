import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, AsyncIterator
from claude_code_sdk import query, ClaudeCodeOptions, UserMessage, AssistantMessage, SystemMessage, ResultMessage, TextBlock
from claude_code_sdk.types import PermissionMode, McpStdioServerConfig

logger = logging.getLogger(__name__)

class ClaudeCodeClientWrapper:
    """
    A wrapper around claude_code_sdk.query that provides similar functionality to the
    standard Anthropic client but uses Claude Code's enhanced capabilities.
    Handles async operations internally to provide a synchronous interface.
    """
    
    def __init__(self, version_dir: str, claude_config=None, disabled_tools=None):
        self.version_dir = version_dir
        self.claude_config = claude_config
        self.disabled_tools = disabled_tools or []
        self.client_dir = os.path.join(version_dir, "client")
        self.request_counter = 0
        self.session_id = None
        self._loop = None
        
        # Parse disabled tools into server-level and function-level
        self.disabled_servers = set()
        self.disabled_functions = {}  # server_name -> set of function names
        
        logger.info(f"Parsing disabled tools: {self.disabled_tools}")
        for tool in self.disabled_tools:
            if tool == "all":
                self.disabled_servers.add("all")
                logger.info(f"Disabled all servers")
            elif ":" in tool:
                # Function-level disabling: server_name:function_name
                server_name, function_name = tool.split(":", 1)
                if server_name not in self.disabled_functions:
                    self.disabled_functions[server_name] = set()
                self.disabled_functions[server_name].add(function_name)
                logger.info(f"Disabled function {function_name} from server {server_name}")
            else:
                # Server-level disabling
                self.disabled_servers.add(tool)
                logger.info(f"Disabled server {tool}")
        
        logger.info(f"Final disabled_servers: {self.disabled_servers}")
        logger.info(f"Final disabled_functions: {self.disabled_functions}")
        
        # Create client directory if it doesn't exist
        os.makedirs(self.client_dir, exist_ok=True)
        logger.info(f"Claude Code client wrapper initialized. Saving requests/responses to: {self.client_dir}")
    
    def _load_mcp_config(self) -> Dict[str, McpStdioServerConfig]:
        """Load MCP server configuration from .mcp.json file."""
        mcp_servers = {}
        
        # Look for .mcp.json in current directory and project root
        search_paths = [
            os.path.join(os.getcwd(), ".mcp.json"),
            os.path.join(os.path.dirname(self.version_dir), ".mcp.json"),
            os.path.join(os.path.dirname(os.path.dirname(self.version_dir)), ".mcp.json")
        ]
        
        for mcp_config_path in search_paths:
            if os.path.exists(mcp_config_path):
                logger.info(f"Loading MCP configuration from: {mcp_config_path}")
                try:
                    with open(mcp_config_path, 'r') as f:
                        mcp_config = json.load(f)
                    
                    # Convert to McpStdioServerConfig format
                    # Resolve relative paths in args relative to the .mcp.json location
                    config_dir = os.path.dirname(mcp_config_path)
                    
                    for server_name, server_config in mcp_config.get("mcpServers", {}).items():
                        # Check if this server should be completely disabled
                        if "all" in self.disabled_servers or server_name in self.disabled_servers:
                            logger.info(f"Skipping disabled MCP server: {server_name}")
                            continue
                            
                        # Set environment variable for disabled functions if any
                        disabled_funcs = self.disabled_functions.get(server_name, set())
                        env_vars = server_config.get("env", {}).copy()
                        if disabled_funcs and server_name == "tt-metal-tools":
                            logger.info(f"Server {server_name} will have disabled functions: {disabled_funcs}")
                            env_vars["DISABLED_FUNCTIONS"] = ",".join(disabled_funcs)
                        
                        # Process the regular server configuration
                        args = []
                        for arg in server_config.get("args", []):
                            if not os.path.isabs(arg) and (arg.endswith('.py') or '/' in arg):
                                # This looks like a relative path, resolve relative to cwd if specified
                                cwd = server_config.get("cwd")
                                if cwd:
                                    # Resolve relative to the cwd directory
                                    args.append(os.path.join(cwd, arg))
                                else:
                                    # Resolve relative to config directory
                                    args.append(os.path.abspath(os.path.join(config_dir, arg)))
                            else:
                                args.append(arg)
                        
                        # Handle working directory by wrapping command if needed
                        command = server_config.get("command", "")
                        cwd = server_config.get("cwd")
                        if cwd:
                            # Wrap command to change directory
                            if args:
                                args_str = " ".join(f'"{arg}"' for arg in args)
                                command_with_args = f"{command} {args_str}"
                            else:
                                command_with_args = command
                            command = "sh"
                            args = ["-c", f"cd {cwd} && {command_with_args}"]
                        
                        # Create server configuration with supported fields
                        mcp_servers[server_name] = McpStdioServerConfig(
                            command=command,
                            args=args,
                            env=env_vars
                        )
                    
                    logger.info(f"Loaded {len(mcp_servers)} MCP servers: {list(mcp_servers.keys())}")
                    for name, config in mcp_servers.items():
                        logger.info(f"MCP server {name} config: {dict(config)}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to load MCP configuration from {mcp_config_path}: {e}")
        
        if not mcp_servers:
            if "all" in self.disabled_servers:
                logger.info("All MCP tools disabled by --disable-tools flag")
            else:
                logger.info("No MCP configuration found - will use Claude Code's default settings")
        else:
            # Log summary of disabled functions
            if self.disabled_functions:
                for server, funcs in self.disabled_functions.items():
                    if server in mcp_servers:
                        logger.info(f"MCP server '{server}' loaded with disabled functions: {list(funcs)}")
        
        return mcp_servers
    
    def save_request_response(self, request_data: Dict[str, Any], response_data: Dict[str, Any]):
        """
        Save a request-response pair to the client directory.
        
        Args:
            request_data: The request data sent to Claude Code
            response_data: The response data received from Claude Code
        """
        self.request_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename with counter and timestamp
        filename_base = f"request_{self.request_counter:03d}_{timestamp}"
        
        # Save request
        request_file = os.path.join(self.client_dir, f"{filename_base}_request.json")
        with open(request_file, 'w', encoding='utf-8') as f:
            json.dump(request_data, f, indent=2, ensure_ascii=False)
        
        # Save response
        response_file = os.path.join(self.client_dir, f"{filename_base}_response.json")
        with open(response_file, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, indent=2, ensure_ascii=False)
        
        # Save combined request-response for easier analysis
        combined_file = os.path.join(self.client_dir, f"{filename_base}_combined.json")
        combined_data = {
            "request": request_data,
            "response": response_data,
            "metadata": {
                "request_number": self.request_counter,
                "timestamp": timestamp,
                "request_file": os.path.basename(request_file),
                "response_file": os.path.basename(response_file)
            }
        }
        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved request-response pair {self.request_counter} to {filename_base}")
    
    @property
    def messages(self):
        """Provide messages property for compatibility with existing code."""
        return self.MessagesWrapper(self)
    
    def _run_async(self, coro):
        """Run an async coroutine in a synchronous context."""
        # Create a new event loop every time (simpler, more predictable)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(coro)
            return result
        except Exception as e:
            logger.error(f"Error during async execution: {type(e).__name__}: {e}")
            raise
        finally:
            loop.close()
            asyncio.set_event_loop(None)
    
    class MessagesWrapper:
        """Wrapper to provide compatibility with the standard Anthropic client interface."""
        
        def __init__(self, wrapper):
            self.wrapper = wrapper
        
        def create(self, **kwargs):
            """
            Create a message using claude_code_sdk.query with compatibility for standard Anthropic interface.
            """
            # Extract standard parameters
            model = kwargs.get("model")
            system = kwargs.get("system")
            messages = kwargs.get("messages", [])
            max_tokens = kwargs.get("max_tokens")
            
            # Convert messages to prompt format
            prompt_parts = []
            for message in messages:
                role = message.get("role", "")
                content = message.get("content", "")
                if role == "user":
                    prompt_parts.append(content)
                elif role == "assistant":
                    prompt_parts.append(f"Assistant: {content}")
            
            prompt = "\n\n".join(prompt_parts)
            
            # Load MCP configuration
            mcp_servers = self.wrapper._load_mcp_config()
            
            # Create Claude Code options
            options = ClaudeCodeOptions(
                system_prompt=system,
                model=model,
                max_thinking_tokens=max_tokens or 8000,
                continue_conversation=self.wrapper.session_id is not None,
                permission_mode='bypassPermissions',  # Allow all tools for automated execution
                cwd=self.wrapper.version_dir,
                mcp_servers=mcp_servers
            )

            if mcp_servers:
                logger.info(f"Using MCP servers: {list(mcp_servers.keys())}")
            else:
                logger.info("No MCP servers configured - using Claude Code's default settings")
            
            # Prepare request data for logging
            request_data = {
                "prompt": prompt,
                "options": {
                    "system_prompt": system,
                    "model": model,
                    "max_thinking_tokens": options.max_thinking_tokens,
                    "continue_conversation": options.continue_conversation,
                    "permission_mode": options.permission_mode,
                    "cwd": str(options.cwd),
                    "mcp_servers": {name: dict(config) for name, config in mcp_servers.items()}
                },
                "original_kwargs": kwargs,
                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"prompt: {prompt}")
            
            # Run the async query using our helper method
            response = self.wrapper._run_async(self._query_claude_code(prompt, options))
            response_data = self._format_response_data(response)
            
            # Save the request-response pair
            self.wrapper.save_request_response(request_data, response_data)
            
            # Return a compatible response object
            return self._create_compatible_response(response)
        
        async def _query_claude_code(self, prompt: str, options: ClaudeCodeOptions):
            """Execute the claude_code_sdk.query and collect results."""
            messages = []
            result_message = None
            
            async for message in query(prompt=prompt, options=options):
                messages.append(message)
                if isinstance(message, ResultMessage):
                    result_message = message
                    self.wrapper.session_id = message.session_id
            
            return {
                "messages": messages,
                "result": result_message
            }
        
        def _format_response_data(self, response):
            """Format the response data for logging."""
            response_data = {
                "messages": [],
                "result": None,
                "tool_calls": [],
                "timestamp": datetime.now().isoformat()
            }
            
            for message in response["messages"]:
                if isinstance(message, UserMessage):
                    response_data["messages"].append({
                        "type": "user",
                        "content": message.content
                    })
                elif isinstance(message, AssistantMessage):
                    content_text = ""
                    tool_calls = []
                    
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            content_text += block.text
                        elif hasattr(block, 'type') and block.type == 'tool_use':
                            # Handle tool use blocks
                            tool_call = {
                                "id": getattr(block, 'id', None),
                                "name": getattr(block, 'name', None),
                                "input": getattr(block, 'input', {})
                            }
                            tool_calls.append(tool_call)
                            response_data["tool_calls"].append(tool_call)
                            
                            # Print tool call to stdout for immediate visibility
                            print(f"\n🛠️  TOOL CALL: {tool_call['name']}")
                            print(f"   Parameters: {json.dumps(tool_call['input'], indent=2)}")
                            
                    response_data["messages"].append({
                        "type": "assistant",
                        "content": content_text,
                        "tool_calls": tool_calls
                    })
                elif isinstance(message, SystemMessage):
                    msg_data = {
                        "type": "system",
                        "subtype": message.subtype,
                        "data": message.data
                    }
                    
                    # Check if this is a tool result message
                    if message.subtype == "tool_result" and hasattr(message, 'data'):
                        if isinstance(message.data, dict):
                            tool_name = message.data.get('name', 'unknown')
                            tool_result = message.data.get('content', message.data.get('result', 'No result'))
                            
                            # Print tool result to stdout for immediate visibility
                            print(f"\n✅ TOOL RESULT: {tool_name}")
                            if isinstance(tool_result, (dict, list)):
                                print(f"   Result: {json.dumps(tool_result, indent=2)[:500]}...")
                            else:
                                print(f"   Result: {str(tool_result)[:500]}...")
                    
                    response_data["messages"].append(msg_data)
                elif isinstance(message, ResultMessage):
                    response_data["result"] = {
                        "subtype": message.subtype,
                        "duration_ms": message.duration_ms,
                        "duration_api_ms": message.duration_api_ms,
                        "is_error": message.is_error,
                        "num_turns": message.num_turns,
                        "session_id": message.session_id,
                        "total_cost_usd": message.total_cost_usd,
                        "usage": message.usage,
                        "result": message.result
                    }
            
            return response_data
        
        def _create_compatible_response(self, response):
            """Create a response object compatible with the existing code."""
            # Find the last assistant message
            assistant_content = ""
            for message in response["messages"]:
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            assistant_content = block.text
                            break
            
            # Create a simple response object that mimics the Anthropic client response
            class CompatibleResponse:
                def __init__(self, content_text, result_message):
                    self.content = [type('ContentBlock', (), {'text': content_text})()]
                    self.model = result_message.session_id if result_message else None
                    self.usage = result_message.usage if result_message else {}
            
            return CompatibleResponse(assistant_content, response["result"])
