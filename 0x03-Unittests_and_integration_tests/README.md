# ALX Backend Python - Unit Testing

This repository contains Python exercises and projects for learning backend development with Python.

## 0x03 - Unittests and Integration Tests

This directory contains tests for utility functions, including parameterized unit tests for `access_nested_map`.

### Test: Parameterize a Unit Test

- Implemented a test class `TestAccessNestedMap` using `unittest`.
- Used `@parameterized.expand` decorator to run multiple input cases.
- Tested the `access_nested_map` function with nested dictionaries and paths.
- Test file: `test_utils.py`
- Run tests with:  
  ```bash
  python -m unittest test_utils.py
