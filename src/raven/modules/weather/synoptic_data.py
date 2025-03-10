import datetime
from typing import Dict, Any

import openmeteo_requests  # type: ignore
import requests
from raven.core.api_base import collect_keys
from retry_requests import retry

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


def gather_synoptic(lat: float, lon: float, radius_mi: float = 10) -> Dict:
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
        "limit": 5,
        "units": "metric,temp|C,speed|kph,pres|mb,height|m,precip|mm,alti|pa",
    }
    req = requests.get(api_request_url, params=api_arguments)
    data = req.json()
    return data  # type: ignore


def correct_synoptic(data: Dict[str, Any]) -> tuple[dict[str, Any], str, str, int]:
    """
    Corrects the data from Synoptic (units, date/time)
    :param data: Weather data from Synoptic API
    :return: Corrected weather data
    """
    # Apply Unit Corrections
    # (snow)

    # (visibility) statute miles > km

    # Convert datetime to epoch using DateTime
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    date = (
        datetime.datetime.strptime(data["data"]["time"], time_format)
        .date()
        .strftime("%Y-%m-%d")
    )
    time = (
        datetime.datetime.strptime(data["data"]["time"], time_format)
        .time()
        .strftime("%H:%M:%S")
    )
    utc_epoch = int(
        datetime.datetime.strptime(data["data"]["time"], time_format).timestamp()
    )
    return data, date, time, utc_epoch
