# Simple Python Logger

A lightweight, colorful logging utility for Python applications.

## Features

- 5 logging levels (CRITICAL, ERROR, WARNING, INFO, DEBUG)
- Color-coded output for better visibility
- Level-based indentation for improved readability
- Simple and intuitive API
- Customizable output stream

## Installation

No installation required - just copy the `logger.py` file to your project.

## Usage

### Basic Usage

```python
from logger import Logger

# Create a logger (default level is 4, showing all messages)
logger = Logger()

# Log messages at different levels
logger.critical("Critical system failure!")
logger.error("An error occurred")
logger.warning("This is a warning")
logger.info("Informational message")
logger.debug("Debug information")
```

### Setting Log Level

You can control which messages are displayed by setting the maximum log level:

```python
# Create a logger that only shows messages with level <= 2 (CRITICAL, ERROR, WARNING)
logger = Logger(level=2)

# Or change the level later
logger.set_level(1)  # Now only shows CRITICAL and ERROR
```

### Log Levels

| Level | Name      | Color   | Description                                       |
|-------|-----------|---------|---------------------------------------------------|
| 0     | CRITICAL  | Red     | Critical errors that cause application to abort   |
| 1     | ERROR     | Yellow  | Error conditions                                  |
| 2     | WARNING   | Magenta | Warning conditions                                |
| 3     | INFO      | Green   | Informational messages                            |
| 4     | DEBUG     | Blue    | Detailed debug information                        |

### Custom Output

By default, the logger writes to `stdout`, but you can specify a different output stream:

```python
import sys

# Log to stderr instead
logger = Logger(output=sys.stderr)

# Or log to a file
with open('app.log', 'w') as log_file:
    logger = Logger(output=log_file)
    logger.info("This message goes to the file")
```

## Example

See `example_usage.py` for a complete usage example.

## Running Tests

Tests are included in `test.py`. Run them with:

```
python3 test.py
```

## License

This project is open source and available for any use.
