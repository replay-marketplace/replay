import sys
import datetime

class Logger:
    # ANSI color codes
    COLORS = {
        0: '\033[31m',  # Red for critical
        1: '\033[33m',  # Yellow for error
        2: '\033[34m',  # Blue for warning
        3: '\033[32m',  # Green for info
        4: '\033[35m',  # Magenta for debug
    }
    RESET = '\033[0m'  # Reset color
    
    # Level names for better readability
    LEVEL_NAMES = {
        0: 'CRITICAL',
        1: 'ERROR',
        2: 'WARNING',
        3: 'INFO',
        4: 'DEBUG'
    }
    
    def __init__(self, min_level=0, use_colors=True, output=sys.stdout):
        """
        Initialize the logger.
        
        Args:
            min_level (int): Minimum level to log (0-4). 0 is highest priority, 4 is lowest.
            use_colors (bool): Whether to use colors in the output.
            output: File-like object to write logs to (default: sys.stdout).
        """
        self.min_level = min_level
        self.use_colors = use_colors
        self.output = output
    
    def log(self, level, message):
        """
        Log a message at the specified level.
        
        Args:
            level (int): Log level (0-4). 0 is highest priority, 4 is lowest.
            message (str): Message to log.
        """
        if level > self.min_level:
            return
        
        # Create timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create indentation based on level
        indent = ' ' * level
        
        # Format the log message
        level_name = self.LEVEL_NAMES.get(level, f'LEVEL{level}')
        formatted_message = f"[{timestamp}] [{level_name}] {indent}{message}"
        
        # Add color if enabled
        if self.use_colors:
            color = self.COLORS.get(level, '')
            formatted_message = f"{color}{formatted_message}{self.RESET}"
        
        # Write to output
        print(formatted_message, file=self.output)
    
    def critical(self, message):
        """Log a critical message (level 0)."""
        self.log(0, message)
    
    def error(self, message):
        """Log an error message (level 1)."""
        self.log(1, message)
    
    def warning(self, message):
        """Log a warning message (level 2)."""
        self.log(2, message)
    
    def info(self, message):
        """Log an info message (level 3)."""
        self.log(3, message)
    
    def debug(self, message):
        """Log a debug message (level 4)."""
        self.log(4, message)
