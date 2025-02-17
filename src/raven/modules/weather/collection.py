import json
import requests
from typing import Dict, Any, cast


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


def collect_tomorrow(apikey: str) -> Dict[str, Any]:
    url = (
        f"https://api.tomorrow.io/v4/weather/realtime?location=toronto&apikey={apikey}"
    )
    headers = {"accept": "application/json", "accept-encoding": "deflate, gzip, br"}
    response = requests.get(url, headers=headers)

    return cast(Dict[str, Any], response.json())
