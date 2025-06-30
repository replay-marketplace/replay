import os
import json
import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class ClientWrapper:
    """
    A wrapper around the Anthropic client that saves all requests and responses
    to the version directory for debugging and analysis.
    """
    
    def __init__(self, client, version_dir: str):
        self.client = client
        self.version_dir = version_dir
        self.client_dir = os.path.join(version_dir, "client")
        self.request_counter = 0
        
        # Create client directory if it doesn't exist
        os.makedirs(self.client_dir, exist_ok=True)
        logger.info(f"Client wrapper initialized. Saving requests/responses to: {self.client_dir}")
    
    def save_request_response(self, request_data: Dict[str, Any], response_data: Dict[str, Any]):
        """
        Save a request-response pair to the client directory.
        
        Args:
            request_data: The request data sent to the client
            response_data: The response data received from the client
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
        """Proxy to the underlying client's messages property."""
        return self.MessagesWrapper(self.client.messages, self)
    
    class MessagesWrapper:
        """Wrapper around the client's messages object to intercept create calls."""
        
        def __init__(self, messages, wrapper):
            self.messages = messages
            self.wrapper = wrapper
        
        def create(self, **kwargs):
            """
            Intercept the create call, save request/response, and return the response.
            """
            # Extract the request data
            request_data = {
                "model": kwargs.get("model"),
                "system": kwargs.get("system"),
                "messages": kwargs.get("messages", []),
                "max_tokens": kwargs.get("max_tokens"),
                "timestamp": datetime.now().isoformat()
            }
            
            # Make the actual request
            response = self.messages.create(**kwargs)
            
            # Extract response data
            response_data = {
                "content": [{"text": content.text} for content in response.content] if hasattr(response, 'content') else [],
                "model": getattr(response, 'model', None),
                "usage": getattr(response, 'usage', {}).__dict__ if hasattr(getattr(response, 'usage', None), '__dict__') else getattr(response, 'usage', None),
                "timestamp": datetime.now().isoformat()
            }
            
            # Save the request-response pair
            self.wrapper.save_request_response(request_data, response_data)
            
            return response 