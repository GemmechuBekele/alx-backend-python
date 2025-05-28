#!/usr/bin/env python3
import requests
"""
Utils module with access_nested_map
"""

def access_nested_map(nested_map, path):
    """Access a nested map with a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def get_json(url):
    response = requests.get(url)
    return response.json()