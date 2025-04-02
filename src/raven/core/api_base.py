import os
import json
from typing import Dict, Any


def collect_keys(file_path: str = "../config/api_keys.json") -> Dict[str, Any]:
    """
    Reads API keys from JSON file

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary representing the JSON data, or None if an error occurs.
    """
    with open(file_path, "r") as file:
        data: Dict[str, Any] = json.load(file)

    return data


def ping_website(address: str) -> bool:
    """
    Pings a website address and prints the output.

    Args:
        address: The website address or IP address to ping.
    """
    command = f"ping {address}"
    response = os.system(command)

    if response == 0:
        return True
    else:
        return False  # Website unreachable
