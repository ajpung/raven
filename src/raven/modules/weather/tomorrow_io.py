from typing import Dict, Any, cast

import openmeteo_requests  # type: ignore
import requests
from retry_requests import retry  # type: ignore

from raven.core.api_base import collect_keys


def collect_tomorrow(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from Tomorrow.io

    :param apikey: API key for Tomorrow.io
    :return: Weather data from Tomorrow.io API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["tomorrow-io"]
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={apikey}&units=metric"
    response = requests.get(url)
    return cast(Dict[str, Any], response.json())
