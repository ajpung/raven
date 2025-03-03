from typing import Dict, Any, cast

import openmeteo_requests  # type: ignore
import requests
from retry_requests import retry  # type: ignore

from raven.core.api_base import collect_keys

"""
'queryCost': 1
'latitude': 38.422508
'longitude': -85.797633
'resolvedAddress': '38.422508,-85.797633'
'address': '38.422508,-85.797633'
'timezone': 'America/Kentucky/Louisville'
'tzoffset': -5.0
'days': {
    'datetime': '2025-03-03'
    'datetimeEpoch': 1740978000
    'tempmax': 13.3
    'tempmin': -3.1
    'temp': 4.0
    'feelslikemax': 13.3
    'feelslikemin': -5.8
    'feelslike': 3.0
    'dew': -8.6
    'humidity': 42.4
    'precip': 0.0
    'precipprob': 1.0
    'precipcover': 0.0
    'preciptype': None
    'snow': 0.0
    'snowdepth': 0.0
    'windgust': 27.7
    'windspeed': 15.2
    'winddir': 152.7
    'pressure': 1022.2
    'cloudcover': 21.9
    'visibility': 16.1
    'solarradiation': 173.3
    'solarenergy': 15.1
    'uvindex': 6.0
    'severerisk': 10.0
    'sunrise': '07:11:51'
    'sunriseEpoch': 1741003911
    'sunset': '18:38:50'
    'sunsetEpoch': 1741045130
    'moonphase': 0.13
    'conditions': 'Partially cloudy'
    'description': 'Becoming cloudy in the afternoon.'
    'icon': 'partly-cloudy-day'
    'stations': ['KFTK', 'KLOU', 'AU953', 'KSDF']
    'source': 'comb'}
'stations': {
    'KFTK': {
        'distance': 60090.0
        'latitude': 37.9
        'longitude': -85.97
        'useCount': 0
        'id': 'KFTK'
        'name': 'KFTK'
        'quality': 97
        'contribution': 0.0}
    'KJVY': {
        'distance': 8106.0
        'latitude': 38.367
        'longitude': -85.738
        'useCount': 0
        'id': 'KJVY'
        'name': 'Clark Regional Airport IN US NWS/FAA'
        'quality': 0
        'contribution': 0.0}
    'E0284': {
        'distance': 12046.0
        'latitude': 38.332
        'longitude': -85.873
        'useCount': 0
        'id': 'E0284'
        'name': 'EW0284 Floyds Knobs IN US'
        'quality': 0
        'contribution': 0.0}
    'KLOU': {
        'distance': 25148.0
        'latitude': 38.22
        'longitude': -85.67
        'useCount': 0
        'id': 'KLOU'
        'name': 'KLOU'
        'quality': 100
        'contribution': 0.0}
    'AU953': {
        'distance': 12718.0
        'latitude': 38.311
        'longitude': -85.83
        'useCount': 0
        'id': 'AU953'
        'name': 'N9OKI New Albany IN US'
        'quality': 0
        'contribution': 0.0}
    'KSDF': {
        'distance': 27635.0
        'latitude': 38.18
        'longitude': -85.73
        'useCount': 0
        'id': 'KSDF'
        'name': 'KSDF'
        'quality': 100
        'contribution': 0.0}
    'IN018': {
        'distance': 17654.0
        'latitude': 38.269
        'longitude': -85.746
        'useCount': 0
        'id': 'IN018'
        'name': 'Jeffersonville IN US INDOT'
        'quality': 0
        'contribution': 0.0}
    }
'currentConditions': {
    'datetime': '17:15:00'
    'datetimeEpoch': 1741040100
    'temp': 12.6
    'feelslike': 12.6
    'humidity': 21.9
    'dew': -8.7
    'precip': 0.0
    'precipprob': 0.0
    'snow': 0.0
    'snowdepth': 0.0
    'preciptype': None
    'windgust': 12.7
    'windspeed': 10.1
    'winddir': 168.0
    'pressure': 1002.0
    'visibility': 16.0
    'cloudcover': 0.0
    'solarradiation': 141.0
    'solarenergy': 0.5
    'uvindex': 1.0
    'conditions': 'Clear'
    'icon': 'clear-day'
    'stations': ['KJVY', 'E0284', 'IN018']
    'source': 'obs'
    'sunrise': '07:11:51'
    'sunriseEpoch': 1741003911
    'sunset': '18:38:50'
    'sunsetEpoch': 1741045130
    'moonphase': 0.13}
}
"""


def gather_visualcrossing(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from Visual Crossing

    :return: Weather data from Visual Crossing API
    """
    # Build the API URL
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    url = f"{base_url}/{lat},{lon}/today"
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["visual-crossing"]
    # Parameters for the request
    params = {
        "unitGroup": "metric",  # or 'us' for imperial units
        "include": "current",
        "key": apikey,
        "contentType": "json",
    }
    response = requests.get(url, params=params)
    return cast(Dict[str, Any], response.json())


# def correct_visualcrossing(lat: float, lon: float) -> Dict[str, Any]:
