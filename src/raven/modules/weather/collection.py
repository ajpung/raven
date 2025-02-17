import json
import requests
from typing import Dict, Any


def collect_tomorrow(apikey: str):  # type:ignore
    """
    Collects weather data from Tomorrow.io API

    Args:
        apikey: API key for Tomorrow.io

    Returns:
        dict: Weather data from Tomorrow.io API
    """
    url = (
        f"https://api.tomorrow.io/v4/weather/realtime?location=toronto&apikey={apikey}"
    )
    headers = {"accept": "application/json", "accept-encoding": "deflate, gzip, br"}
    response = requests.get(url, headers=headers)

    return response.json()


def collect_api_key(file_path: str = "./docs/api_keys.json") -> Dict[str, str]:
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
