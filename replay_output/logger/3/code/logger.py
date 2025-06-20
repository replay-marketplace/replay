class Logger:
    # ANSI color codes
    COLORS = {
        0: "\033[31m",  # Red for critical (level 0)
        1: "\033[33m",  # Yellow for error (level 1)
        2: "\033[34m",  # Blue for warning (level 2)
        3: "\033[32m",  # Green for info (level 3)
        4: "\033[37m",  # White for debug (level 4)
    }
    RESET = "\033[0m"  # Reset color
    
    LEVEL_NAMES = {
        0: "CRITICAL",
        1: "ERROR",
        2: "WARNING",
        3: "INFO",
        4: "DEBUG"
    }
    
    def __init__(self, level=3):
        """
        Initialize the logger with a default log level of 3 (INFO).
        Only messages with level <= the current level will be logged.
        """
        self.level = level
    
    def set_level(self, level):
        """
        Set the logging level (0-4).
        """
        if level not in range(5):
            raise ValueError("Log level must be between 0 and 4")
        self.level = level
    
    def log(self, message, level=3):
        """
        Log a message at the specified level.
        """
        if level not in range(5):
            raise ValueError("Log level must be between 0 and 4")
        
        if level <= self.level:
            indent = " " * level
            level_name = self.LEVEL_NAMES[level]
            print(f"{self.COLORS[level]}[{level_name}] {indent}{message}{self.RESET}")
    
    def critical(self, message):
        """
        Log a critical message (level 0).
        """
        self.log(message, 0)
    
    def error(self, message):
        """
        Log an error message (level 1).
        """
        self.log(message, 1)
    
    def warning(self, message):
        """
        Log a warning message (level 2).
        """
        self.log(message, 2)
    
    def info(self, message):
        """
        Log an info message (level 3).
        """
        self.log(message, 3)
    
    def debug(self, message):
        """
        Log a debug message (level 4).
        """
        self.log(message, 4)