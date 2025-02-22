from typing import Dict, Any, cast

import openmeteo_requests  # type: ignore
import requests
from retry_requests import retry  # type: ignore

from raven.core.api_base import collect_keys


def collect_viscrs(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from Visual Crossing

    :return: Weather data from Visual Crossing API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["visual-crossing"]
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat}%2C%20{lon}?unitGroup=metric&&include=current&key={apikey}&contentType=json"
    response = requests.get(url)
    return cast(Dict[str, Any], response.json())
