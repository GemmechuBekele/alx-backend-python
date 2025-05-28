# alx-backend-python: Unit Tests for `access_nested_map`

This repository contains backend Python exercises and projects, including unit and integration testing. In this specific directory (`0x03-Unittests_and_integration_tests`), we focus on writing unit tests using Python's `unittest` framework along with the `parameterized` module.

## 📁 Directory Structure

0x03-Unittests_and_integration_tests/
├── utils.py # Contains the access_nested_map function
├── test_utils.py # Unit tests for access_nested_map
└── README.md # Project documentation (this file)

## 🔧 Function Overview

### `access_nested_map`

```python
def access_nested_map(nested_map, path):
    """Access a nested map using a tuple of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map

python test_utils.py

output:
test_access_nested_map_0 (__main__.TestAccessNestedMap) ... ok
test_access_nested_map_1 (__main__.TestAccessNestedMap) ... ok
test_access_nested_map_2 (__main__.TestAccessNestedMap) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```