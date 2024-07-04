import re
import os

def sanitize(filename: str, replacement: str = '_') -> str:
    """
    Sanitize a filename by removing or replacing invalid characters.
    
    :param filename: The original filename to sanitize.
    :param replacement: The character to replace invalid characters with.
    :return: A sanitized filename.
    """
    # Define a regex pattern for invalid characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
    
    # Replace invalid characters with the replacement character
    sanitized = re.sub(invalid_chars, replacement, filename)
    
    # Remove leading and trailing whitespace
    sanitized = sanitized.strip()
    
    # Ensure the filename is not empty
    if not sanitized:
        raise ValueError("Sanitized filename is empty.")
    
    return sanitized

# Example usage
if __name__ == "__main__":
    original_filename = "example:filename/with\\invalid|characters?.txt"
    sanitized_filename = sanitize(original_filename)
    print(f"Original: {original_filename}")
    print(f"Sanitized: {sanitized_filename}")