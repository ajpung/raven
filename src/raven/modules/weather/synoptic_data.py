import datetime
import json
from typing import Dict, Any, cast

import openmeteo_requests  # type: ignore
import requests
from raven.core.api_base import collect_keys
from retry_requests import retry  # type: ignore

"""
Units taken from Units taken from https://demos.synopticdata.com/variables/index.html

^^^None^^^
latitude: deg
longitude: deg
resolvedAddress: deg, deg
address: deg, deg

timezone: Z
tzoffset: 0.0

^^^currentConditions^^^
datetime: HH:MM:SS
temp: C
humidity: %
dew: C
precip: mm
snow: mm
snowdepth: mm
windgust: km/hr
windspeed: km/hr
winddir: deg
pressure: mb
visibility: statute miles (-0.25 means < 0.25 miles)
cloudcover: %
solarradiation: W/m^2
solarenergy: ?
uvindex: -
cape: ?
cin: ?
conditions: 'Partially cloudy'
sunrise: HH:MM:SS
sunset: HH:MM:SS
moonphase: Fraction
"""


def gather_synoptic(
    lat: float, lon: float, radius_mi: float = 10, n_stations: int = 5
) -> Dict[str, Any]:
    """
    Collects weather data from Synoptic Data

    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return data: Weather data from Synoptic Data API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["synoptic-data"]

    # Build the API URL
    import os

    API_ROOT = "https://api.synopticdata.com/v2/"
    api_request_url = os.path.join(API_ROOT, "stations/latest")
    api_arguments = {
        "token": apikey,
        "radius": f"{lat},{lon},{radius_mi}",
        "limit": n_stations,
        "units": "metric,temp|C,speed|kph,pres|mb,height|m,precip|mm,alti|pa",
    }
    req = requests.get(api_request_url, params=api_arguments)
    data = req.json()
    return data
