import json
import requests
from typing import Dict, Any, cast


def collect_tomorrow(apikey: str) -> Dict[str, Any]:
    url = (
        f"https://api.tomorrow.io/v4/weather/realtime?location=toronto&apikey={apikey}"
    )
    headers = {"accept": "application/json", "accept-encoding": "deflate, gzip, br"}
    response = requests.get(url, headers=headers)

    return cast(Dict[str, Any], response.json())
