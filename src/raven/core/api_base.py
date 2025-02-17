import json
from typing import Dict


def collect_keys(file_path: str = "../docs/api_keys.json") -> Dict[str, str]:
    """
    Reads API keys from JSON file

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary representing the JSON data, or None if an error occurs.
    """
    with open(file_path, "r") as file:
        data: Dict[str, str] = json.load(file)
        return data
