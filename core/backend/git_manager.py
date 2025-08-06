import os
import subprocess
import logging
from typing import Optional
from core.prompt_preprocess2.ir.ir import Opcode

logger = logging.getLogger(__name__)

class GitManager:
    """Manages git operations for replay session folders."""
    
    def __init__(self, version_dir: str):
        """
        Initialize GitManager for a specific version directory.
        
        Args:
            version_dir: Path to the version directory that should be a git repository
        """
        self.version_dir = version_dir
        self._initialized = False
    
    def initialize_repo(self) -> bool:
        """
        Initialize git repository in the version directory.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if git is already initialized
            if os.path.exists(os.path.join(self.version_dir, ".git")):
                logger.info(f"Git repository already exists in {self.version_dir}")
                self._initialized = True
                return True

            # Initialize git repository
            subprocess.run(["git", "init"], cwd=self.version_dir, check=True)
            logger.info(f"Initialized git repository in {self.version_dir}")

            # Configure git user if not already set
            try:
                subprocess.run(["git", "config", "user.name", "Replay System"], cwd=self.version_dir, check=True)
                subprocess.run(["git", "config", "user.email", "replay@system.local"], cwd=self.version_dir, check=True)
            except subprocess.CalledProcessError:
                logger.warning("Failed to configure git user, using existing config")

            self._initialized = True
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initialize git repository: {e}")
            return False
        except FileNotFoundError:
            logger.error("Git not found on system, skipping git initialization")
            return False
    
    def load_existing_repo(self) -> bool:
        """
        Load an existing git repository without reinitializing.
        This is used when loading from a checkpoint where git is already set up.
        
        Returns:
            bool: True if git repository exists and is valid, False otherwise
        """
        try:
            if os.path.exists(os.path.join(self.version_dir, ".git")):
                # Verify it's a valid git repository
                result = subprocess.run(["git", "status"], cwd=self.version_dir, 
                                      capture_output=True, text=True, check=True)
                logger.info(f"Loaded existing git repository in {self.version_dir}")
                self._initialized = True
                return True
            else:
                logger.warning(f"No git repository found in {self.version_dir}")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to load existing git repository: {e}")
            return False
        except FileNotFoundError:
            logger.error("Git not found on system")
            return False
    
    def commit_initial(self) -> bool:
        """
        Make initial commit after compilation.
        Only makes the commit if this is a new repository (no existing commits).
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if this is a new repository (no commits yet)
        try:
            result = subprocess.run(["git", "rev-list", "--count", "HEAD"], 
                                  cwd=self.version_dir, capture_output=True, text=True, check=True)
            commit_count = int(result.stdout.strip())
            if commit_count > 0:
                logger.info(f"Repository already has {commit_count} commits, skipping initial commit")
                return True
        except (subprocess.CalledProcessError, ValueError):
            # If we can't get commit count, assume it's a new repo
            pass
        
        return self._commit_changes("Initial project setup")
    
    def commit_step(self, node_data: dict, opcode: Opcode, step_count: int) -> bool:
        """
        Commit changes after a step execution.
        
        Args:
            node_data: The node data containing operation details
            opcode: The opcode of the executed operation
            step_count: Current step number
            
        Returns:
            bool: True if successful, False otherwise
        """
        commit_message = self._generate_commit_message(node_data, opcode, step_count)
        return self._commit_changes(commit_message)
    
    def _commit_changes(self, commit_message: str) -> bool:
        """
        Commit all changes with the given message.
        
        Args:
            commit_message: The commit message to use
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._initialized:
            logger.warning("Git repository not initialized, skipping commit")
            return False
            
        try:
            # Add all files to git
            subprocess.run(["git", "add", "."], cwd=self.version_dir, check=True)
            
            # Check if there are any changes to commit
            result = subprocess.run(["git", "status", "--porcelain"], cwd=self.version_dir, 
                                  capture_output=True, text=True, check=True)
            if not result.stdout.strip():
                logger.debug("No changes to commit")
                return True

            # Commit changes
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.version_dir, check=True)
            logger.info(f"Git commit: {commit_message}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to commit changes: {e}")
            return False
        except FileNotFoundError:
            logger.error("Git not found on system, skipping commit")
            return False
    
    def _generate_commit_message(self, node_data: dict, opcode: Opcode, step_count: int) -> str:
        """
        Generate a descriptive commit message based on the node and opcode.
        
        Args:
            node_data: The node data containing operation details
            opcode: The opcode of the executed operation
            step_count: Current step number
            
        Returns:
            str: The generated commit message
        """
        opcode_name = opcode.name.lower()
        
        # Get node description or contents for more context
        node_description = ""
        if 'contents' in node_data:
            contents = node_data['contents']
            if isinstance(contents, dict):
                if 'path' in contents:
                    node_description = f" - {contents['path']}"
                elif 'content' in contents:
                    # Truncate content for commit message
                    content_preview = str(contents['content'])[:50]
                    if len(str(contents['content'])) > 50:
                        content_preview += "..."
                    node_description = f" - {content_preview}"
                elif 'prompt' in contents:
                    prompt_preview = str(contents['prompt'])[:50]
                    if len(str(contents['prompt'])) > 50:
                        prompt_preview += "..."
                    node_description = f" - {prompt_preview}"
        
        # Handle specific opcodes with more detailed messages
        if opcode == Opcode.TEMPLATE:
            template_path = node_data.get('contents', {}).get('path', 'unknown template')
            return f"Step {step_count}: Load template {template_path}"
        elif opcode == Opcode.DOCS:
            docs_path = node_data.get('contents', {}).get('path', 'unknown docs')
            return f"Step {step_count}: Load docs {docs_path}"
        elif opcode == Opcode.PROMPT:
            return f"Step {step_count}: LLM prompt{node_description}"
        elif opcode == Opcode.RUN:
            return f"Step {step_count}: Run command{node_description}"
        elif opcode == Opcode.CONDITIONAL:
            return f"Step {step_count}: Conditional branch{node_description}"
        elif opcode == Opcode.FIX:
            return f"Step {step_count}: Fix issue{node_description}"
        elif opcode == Opcode.EXIT:
            return f"Step {step_count}: Exit program{node_description}"
        elif opcode == Opcode.DEBUG_LOOP:
            return f"Step {step_count}: Debug loop{node_description}"
        elif opcode == Opcode.READ_ONLY:
            return f"Step {step_count}: Read-only operation{node_description}"
        else:
            return f"Step {step_count}: {opcode_name}{node_description}"
    
    def is_initialized(self) -> bool:
        """
        Check if the git repository is initialized.
        
        Returns:
            bool: True if git repository is initialized
        """
        return self._initialized


class MockGitManager:
    """Mock implementation of GitManager for when git operations are disabled."""
    
    def __init__(self, version_dir: str):
        """
        Initialize MockGitManager.
        
        Args:
            version_dir: Path to the version directory (unused but kept for compatibility)
        """
        self.version_dir = version_dir
        self._initialized = True
    
    def initialize_repo(self) -> bool:
        """Mock git repository initialization."""
        logger.info("Git operations disabled - skipping repository initialization")
        return True
    
    def load_existing_repo(self) -> bool:
        """Mock loading of existing git repository."""
        logger.info("Git operations disabled - skipping existing repository load")
        return True
    
    def commit_initial(self) -> bool:
        """Mock initial commit after compilation."""
        logger.info("Git operations disabled - skipping initial commit")
        return True
    
    def commit_step(self, node_data: dict, opcode: Opcode, step_count: int) -> bool:
        """Mock commit after step execution."""
        commit_message = self._generate_commit_message(node_data, opcode, step_count)
        logger.info(f"Git operations disabled - would commit: {commit_message}")
        return True
    
    def _generate_commit_message(self, node_data: dict, opcode: Opcode, step_count: int) -> str:
        """Generate commit message (same logic as GitManager for consistency)."""
        opcode_name = opcode.name.lower()
        
        # Get node description or contents for more context
        node_description = ""
        if 'contents' in node_data:
            contents = node_data['contents']
            if isinstance(contents, dict):
                if 'path' in contents:
                    node_description = f" - {contents['path']}"
                elif 'content' in contents:
                    # Truncate content for commit message
                    content_preview = str(contents['content'])[:50]
                    if len(str(contents['content'])) > 50:
                        content_preview += "..."
                    node_description = f" - {content_preview}"
                elif 'prompt' in contents:
                    prompt_preview = str(contents['prompt'])[:50]
                    if len(str(contents['prompt'])) > 50:
                        prompt_preview += "..."
                    node_description = f" - {prompt_preview}"
        
        # Handle specific opcodes with more detailed messages
        if opcode == Opcode.TEMPLATE:
            template_path = node_data.get('contents', {}).get('path', 'unknown template')
            return f"Step {step_count}: Load template {template_path}"
        elif opcode == Opcode.DOCS:
            docs_path = node_data.get('contents', {}).get('path', 'unknown docs')
            return f"Step {step_count}: Load docs {docs_path}"
        elif opcode == Opcode.PROMPT:
            return f"Step {step_count}: LLM prompt{node_description}"
        elif opcode == Opcode.RUN:
            return f"Step {step_count}: Run command{node_description}"
        elif opcode == Opcode.CONDITIONAL:
            return f"Step {step_count}: Conditional branch{node_description}"
        elif opcode == Opcode.FIX:
            return f"Step {step_count}: Fix issue{node_description}"
        elif opcode == Opcode.EXIT:
            return f"Step {step_count}: Exit program{node_description}"
        elif opcode == Opcode.DEBUG_LOOP:
            return f"Step {step_count}: Debug loop{node_description}"
        elif opcode == Opcode.READ_ONLY:
            return f"Step {step_count}: Read-only operation{node_description}"
        else:
            return f"Step {step_count}: {opcode_name}{node_description}"
    
    def is_initialized(self) -> bool:
        """Mock check if git repository is initialized."""
        return True