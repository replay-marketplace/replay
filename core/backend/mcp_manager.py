import os
import json
import subprocess
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class MCPManager:
    """Manages MCP servers for the replay system."""
    
    def __init__(self):
        self.claude_settings_path = Path.home() / ".claude" / "settings.json"
        self.mcp_processes = {}
        
    def ensure_tt_metal_tools(self, database_dir: Optional[str] = None) -> bool:
        """Ensure TT-Metal tools MCP server is configured and running."""
        # Default database directory
        if database_dir is None:
            database_dir = Path(__file__).parent.parent.parent / "tools/api_database_tools/tools/"
        
        database_dir = Path(database_dir)
        # Check/build databases if needed
        sig_db = database_dir / "api_signatures_db.json"
        impl_db = database_dir / "api_impl_db.json"
        
        if not sig_db.exists() or not impl_db.exists():
            logger.info("API databases not found. Building them...")
            return 0
            #self._build_databases(database_dir)
        
        # Update Claude settings
        self._update_claude_settings(sig_db, impl_db)
        
        # Start MCP server
        return self._start_mcp_server(sig_db, impl_db)
    
    def _build_databases(self, database_dir: Path):
        """Build API databases from TT-Metal repository."""
        database_dir.mkdir(parents=True, exist_ok=True)
        
        tt_metal_path = os.environ.get("TT_METAL_HOME")
        if not tt_metal_path:
            raise ValueError(
                "TT_METAL_HOME environment variable not set. "
                "Please set it to your tt-metal repository path."
            )
        
        # Build signature database
        logger.info("Building API signature database...")
        subprocess.run([
            "python", "-m", "api_database_tools.db_generation.build_api_signature_db",
            "--tt-metal-path", tt_metal_path,
            "--output", str(database_dir / "api_signatures_db.json")
        ], check=True)
        
        # Build implementation database
        logger.info("Building API implementation database...")
        subprocess.run([
            "python", "-m", "api_database_tools.db_generation.build_api_impl_db",
            "--tt-metal-path", tt_metal_path,
            "--output", str(database_dir / "api_impl_db.json")
        ], check=True)
        
        logger.info("API databases built successfully")
    
    def _update_claude_settings(self, sig_db: Path, impl_db: Path):
        """Update Claude settings to include TT-Metal MCP server."""
        # Read existing settings
        settings = {}
        if self.claude_settings_path.exists():
            with open(self.claude_settings_path, 'r') as f:
                settings = json.load(f)
        
        # Ensure mcpServers section exists
        if "mcpServers" not in settings:
            settings["mcpServers"] = {}
        
        # Check if tt-metal-tools already configured
        if "tt-metal-tools" in settings["mcpServers"]:
            logger.info("tt-metal-tools already configured in Claude settings")
            return
        
        # Add tt-metal-tools configuration
        settings["mcpServers"]["tt-metal-tools"] = {
        "command": "tt-metal-mcp",  # This is the entry point defined in pyproject.toml
        "env": {
            "API_DATABASE_PATH": str(sig_db),
            "API_IMPL_DATABASE_PATH": str(impl_db)
        }
        }
        
        # Write updated settings
        self.claude_settings_path.parent.mkdir(exist_ok=True)
        with open(self.claude_settings_path, 'w') as f:
            json.dump(settings, f, indent=2)
        
        logger.info("Updated Claude settings with tt-metal-tools MCP server")
    
    def _start_mcp_server(self, sig_db: Path, impl_db: Path) -> bool:
        """Start the MCP server process."""
        # Check if already running
        if "tt-metal-tools" in self.mcp_processes:
            process = self.mcp_processes["tt-metal-tools"]
            if process.poll() is None:
                logger.info("tt-metal-tools MCP server already running")
                return True
        
        # Start the server
        env = os.environ.copy()
        env["API_DATABASE_PATH"] = str(sig_db)
        env["API_IMPL_DATABASE_PATH"] = str(impl_db)
        
        try:
            process = subprocess.Popen(
            ["python", "-m", "api_database_tools.server"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
            self.mcp_processes["tt-metal-tools"] = process
            logger.info("Started tt-metal-tools MCP server")
            return True
        except Exception as e:
            logger.error(f"Failed to start MCP server: {e}")
            return False
    
    def cleanup(self):
        """Stop all MCP server processes."""
        for name, process in self.mcp_processes.items():
            if process.poll() is None:
                logger.info(f"Stopping MCP server: {name}")
                process.terminate()
                process.wait(timeout=5)