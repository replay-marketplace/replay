import os
import json
import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class ClaudeCodeConfig:
    """
    Loads Claude Code configuration from ~/.claude/settings.json and environment variables.
    
    This class handles the migration from standard Anthropic API to Claude Code by:
    1. Reading configuration from ~/.claude/settings.json
    2. Extracting ANTHROPIC_AUTH_TOKEN and ANTHROPIC_BASE_URL from environment
    3. Providing a unified way to access Claude Code settings
    """
    
    def __init__(self):
        self.settings = self._load_settings()
        self.auth_token = self._get_auth_token()
        self.base_url = self._get_base_url()
        
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from ~/.claude/settings.json if it exists."""
        settings_path = Path.home() / ".claude" / "settings.json"
        
        if not settings_path.exists():
            logger.warning(f"Claude Code settings file not found at {settings_path}")
            return {}
            
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
                logger.info(f"Loaded Claude Code settings from {settings_path}")
                return settings
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load Claude Code settings from {settings_path}: {e}")
            return {}
    
    def _get_auth_token(self) -> Optional[str]:
        """
        Get authentication token for Claude Code.
        
        Priority:
        1. ANTHROPIC_AUTH_TOKEN environment variable
        2. ANTHROPIC_AUTH_TOKEN from ~/.claude/settings.json
        3. ANTHROPIC_API_KEY environment variable (fallback for compatibility)
        4. API key helper from settings
        """
        # First check for Claude Code auth token in environment
        auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
        if auth_token:
            logger.info("Using ANTHROPIC_AUTH_TOKEN from environment")
            return auth_token
            
        # Check for Claude Code auth token in settings file
        env_vars = self.settings.get("env", {})
        auth_token_from_settings = env_vars.get("ANTHROPIC_AUTH_TOKEN")
        if auth_token_from_settings:
            logger.info("Using ANTHROPIC_AUTH_TOKEN from ~/.claude/settings.json")
            return auth_token_from_settings
            
        # Fallback to standard API key for compatibility
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            logger.info("Using ANTHROPIC_API_KEY from environment (fallback)")
            return api_key
            
        # Check for API key helper in settings
        api_key_helper = self.settings.get("apiKeyHelper")
        if api_key_helper:
            logger.info("API key helper found in settings, but not implemented in this migration")
            # TODO: Implement API key helper execution if needed
            
        return None
    
    def _get_base_url(self) -> Optional[str]:
        """
        Get base URL for Claude Code API endpoint.
        
        Priority:
        1. ANTHROPIC_BASE_URL environment variable
        2. ANTHROPIC_BASE_URL from ~/.claude/settings.json
        """
        # First check for base URL in environment
        base_url = os.environ.get("ANTHROPIC_BASE_URL")
        if base_url:
            logger.info(f"Using ANTHROPIC_BASE_URL from environment: {base_url}")
            return base_url
            
        # Check for base URL in settings file
        env_vars = self.settings.get("env", {})
        base_url_from_settings = env_vars.get("ANTHROPIC_BASE_URL")
        if base_url_from_settings:
            logger.info(f"Using ANTHROPIC_BASE_URL from ~/.claude/settings.json: {base_url_from_settings}")
            return base_url_from_settings
            
        return None
    
    def is_claude_code_configured(self) -> bool:
        """
        Check if Claude Code is properly configured.
        
        Returns True if both auth token and base URL are available.
        """
        return self.auth_token is not None and self.base_url is not None
    
    def get_client_kwargs(self) -> Dict[str, Any]:
        """
        Get kwargs for initializing the Anthropic client with Claude Code configuration.
        
        Returns:
            Dictionary with client initialization parameters
        """
        kwargs = {}
        
        if self.auth_token:
            kwargs["api_key"] = self.auth_token
            
        if self.base_url:
            kwargs["base_url"] = self.base_url
            
        return kwargs
    
    def get_environment_variables(self) -> Dict[str, str]:
        """
        Get environment variables from Claude Code settings.
        
        Returns:
            Dictionary of environment variables to set
        """
        env_vars = self.settings.get("env", {})
        return env_vars
    
    def log_configuration_status(self):
        """Log the current configuration status for debugging."""
        logger.info("=== Claude Code Configuration Status ===")
        logger.info(f"Settings file loaded: {bool(self.settings)}")
        logger.info(f"Auth token available: {self.auth_token is not None}")
        logger.info(f"Base URL configured: {self.base_url is not None}")
        logger.info(f"Claude Code configured: {self.is_claude_code_configured()}")
        
        if self.settings:
            logger.info(f"Settings keys: {list(self.settings.keys())}")
            
        env_vars = self.get_environment_variables()
        if env_vars:
            logger.info(f"Environment variables from settings: {list(env_vars.keys())}")
        
        logger.info("==========================================") 