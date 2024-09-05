import hashlib


def convert_to_color(string: str) -> str:
    """
    Converts a string to a consistent color in HEX format.

    Args:
        s (str): The string to convert.

    Returns:
        str: The HEX color code.
    """

    # Hash the string to get a consistent number
    hash_value: str = hashlib.md5(string.encode()).hexdigest()
    
    # Use the first 6 characters of the hash to create an RGB color
    color: str = f"#{hash_value[:6]}"
    
    return color
