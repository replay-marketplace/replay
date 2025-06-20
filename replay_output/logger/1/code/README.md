# Simple Python Logger

A lightweight, simple-to-use Python logger with colored output and level-based filtering.

## Features

- 5 logging levels (CRITICAL, ERROR, WARNING, INFO, DEBUG)
- Colored output for easy identification of message types
- Level-based indentation for improved readability
- Configurable minimum log level
- Option to disable colors
- Custom output stream support

## Installation

Simply copy the `simple_logger.py` file to your project.

## Usage

### Basic Usage

```python
from simple_logger import Logger

# Create a logger with default settings
logger = Logger()

# Log messages at different levels
logger.critical("A critical error has occurred!")
logger.error("An error has occurred, but it's not critical.")
logger.warning("This is a warning.")
logger.info("Just some information.")
logger.debug("Debug information for developers.")
```

### Filtering Messages by Level

The logger allows you to set a minimum level. Only messages at that level or higher priority will be displayed:

```python
# Create a logger that only shows messages with level 0-2
# (CRITICAL, ERROR, and WARNING)
logger = Logger(min_level=2)

logger.critical("This will be shown")  # Level 0
logger.error("This will be shown")     # Level 1
logger.warning("This will be shown")   # Level 2
logger.info("This will NOT be shown")  # Level 3
logger.debug("This will NOT be shown") # Level 4
```

### Disabling Colors

```python
# Create a logger without colored output
logger = Logger(use_colors=False)

logger.critical("This will appear without colors")
```

### Custom Output Stream

```python
import sys

# Log to stderr instead of stdout
logger = Logger(output=sys.stderr)

# Log to a file
with open('app.log', 'w') as f:
    file_logger = Logger(use_colors=False, output=f)
    file_logger.info("This goes to the file")
```

## Log Levels

The logger supports 5 logging levels, from highest to lowest priority:

| Level | Method | Description | Color |
|-------|--------|-------------|-------|
| 0 | `critical()` | Critical errors that require immediate attention | Red |
| 1 | `error()` | Error conditions | Yellow |
| 2 | `warning()` | Warning conditions | Blue |
| 3 | `info()` | Informational messages | Green |
| 4 | `debug()` | Detailed debug information | Magenta |

## Running Tests

To run the test suite:

```
python -m unittest test_logger.py
```

## Example

See `example.py` for a complete working example.

## License

This project is free to use for any purpose.
