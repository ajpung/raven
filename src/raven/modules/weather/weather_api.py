import datetime
import json
from typing import Dict, Any, cast

import openmeteo_requests  # type: ignore
import requests
from raven.core.api_base import collect_keys
from pandas import DataFrame
from retry_requests import retry

"""
Units taken from:
    (api example) https://www.weatherapi.com/api-explorer.aspx
    (weather) https://www.weatherapi.com/docs/

------------------------------------------------------
!                     LOCATION                       !
------------------------------------------------------
{
    "location": {
        "name": "London",
        "region": "City of London, Greater London",
        "country": "United Kingdom",
        "lat": 51.5171,
        "lon": -0.1062,
        "tz_id": "Europe/London",
        "localtime_epoch": 1744111535,
        "localtime": "2025-04-08 12:25"
    },
    "current": {
        "last_updated_epoch": 1744110900,
        "last_updated": "2025-04-08 12:15",
        "temp_c": C
        "condition": {
            "text": "Sunny",
            "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
            "code": 1000
        },
        "wind_kph": 12.2,
        "wind_degree": 81,
        "wind_dir": "E",
        "pressure_mb": 1027.0,
        "precip_mm": 0.0,
        "humidity": 44,
        "cloud": 0,
        "feelslike_c": 12.4,
        "windchill_c": 13.3,
        "heatindex_c": 14.1,
        "dewpoint_c": 1.1,
        "vis_km": 10.0,
        "uv": 3.3,
        "gust_kph": 14.1
    }
}
"""


def gather_weatherapi(lat: float, lon: float) -> dict[str, Any]:
    """
    Collects weather data from Accuweather

    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return data: Weather data from Accuweather API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["weather-api"]
    # If location key is found, collect weather data
    # Current
    # url = http://api.weatherapi.com/v1/current.json?key={apikey}&q=31.5/-51.3&aqi=yes
    # Marine
    # url = http://api.weatherapi.com/v1/marine.json?key={apikey}&q=31.5/-51.3&days=1
    # Astronomy
    # url = http://api.weatherapi.com/v1/astronomy.json?key={apikey}&q=31.5/-51.3&dt=2025-04-08
    # Sports
    # url = http://api.weatherapi.com/v1/sports.json?key={apikey}&q=31.5/-51.3

    url = f"http://api.weatherapi.com/v1/current.json?key={apikey}&q={lat},{lon}&aqi=yes&alerts=yes&tides=yes&solar=yes&et0=yes"
    response = requests.get(url)
    data = cast(Dict[str, Any], response.json())
    return data
