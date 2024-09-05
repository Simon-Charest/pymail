from typing import Any


def sort_recursively(data: Any) -> (dict | list | Any):
    if isinstance(data, dict):
        # Sort the dictionary by keys and recursively sort the values
        return {key: sort_recursively(value) for key, value in sorted(data.items())}
    
    elif isinstance(data, list):
        # Sort each item in the list recursively
        return sorted(sort_recursively(datum) for datum in data)
    
    else:
        # Base case: if data is neither dict nor list, return as is
        return data
