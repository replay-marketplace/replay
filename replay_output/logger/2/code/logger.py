import sys

class Logger:
    """
    A simple logger class that outputs messages with different colors based on priority level.
    
    Levels:
    0 - CRITICAL (red)
    1 - ERROR (yellow)
    2 - WARNING (magenta)
    3 - INFO (green)
    4 - DEBUG (blue)
    """
    
    # ANSI color codes
    COLORS = {
        0: "\033[91m",  # Red for CRITICAL
        1: "\033[93m",  # Yellow for ERROR
        2: "\033[95m",  # Magenta for WARNING
        3: "\033[92m",  # Green for INFO
        4: "\033[94m",  # Blue for DEBUG
        "RESET": "\033[0m"
    }
    
    # Level names
    LEVEL_NAMES = {
        0: "CRITICAL",
        1: "ERROR",
        2: "WARNING",
        3: "INFO",
        4: "DEBUG"
    }
    
    def __init__(self, level=4, output=sys.stdout):
        """
        Initialize logger with a maximum level to display.
        
        Args:
            level (int): Maximum level to display (0-4). Default is 4 (all messages).
            output: Output stream. Default is sys.stdout.
        """
        self.level = level
        self.output = output
    
    def log(self, message, level=3):
        """
        Log a message at the specified level.
        
        Args:
            message (str): The message to log.
            level (int): The priority level (0-4). Default is 3 (INFO).
        """
        if level > 4:
            level = 4
        if level < 0:
            level = 0
            
        if level <= self.level:
            indent = ' ' * level
            level_name = self.LEVEL_NAMES[level]
            color = self.COLORS[level]
            reset = self.COLORS["RESET"]
            
            formatted_message = f"{color}[{level_name}]{reset} {indent}{message}\n"
            self.output.write(formatted_message)
            self.output.flush()
    
    def critical(self, message):
        """Log a critical message (level 0)."""
        self.log(message, 0)
    
    def error(self, message):
        """Log an error message (level 1)."""
        self.log(message, 1)
    
    def warning(self, message):
        """Log a warning message (level 2)."""
        self.log(message, 2)
    
    def info(self, message):
        """Log an info message (level 3)."""
        self.log(message, 3)
    
    def debug(self, message):
        """Log a debug message (level 4)."""
        self.log(message, 4)
    
    def set_level(self, level):
        """Set the maximum level to display."""
        self.level = max(0, min(4, level))
