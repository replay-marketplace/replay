# Test Suite for Python Addition Program

This directory contains tests for the Python addition program.

## Running the Tests

You can run all tests using the following command from the project root:

```
python -m unittest discover tests
```

Or run individual test files:

```
python -m unittest tests.test_add_numbers
python -m unittest tests.test_integration
```

## Test Files

- `test_add_numbers.py`: Unit tests for the add_numbers function
- `test_integration.py`: Integration tests for the main program flow
- `__init__.py`: Makes the tests directory a Python package

## Test Coverage

The tests cover:

1. Basic functionality of the add_numbers function
2. Edge cases (zeros, negative numbers, etc.)
3. User input handling
4. Error handling