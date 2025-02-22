from typing import Dict, Any, cast

import openmeteo_requests  # type: ignore
import requests
from retry_requests import retry  # type: ignore

from raven.core.api_base import collect_keys


def collect_openwx(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from OpenWeather

    :return: Weather data from OpenWeather API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["open-weather"]
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units-metric"
    response = requests.get(url)
    return cast(Dict[str, Any], response.json())
