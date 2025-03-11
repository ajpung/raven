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
    (location) https://developer.accuweather.com/accuweather-locations-api/apis/get/locations/v1/cities/geoposition/search
    (weather) https://developer.accuweather.com/accuweather-current-conditions-api/apis/get/currentconditions/v1/%7BlocationKey%7D

***** LOCATION *****
{
  "Version": 1,
  "Key": "2168954",
  "Type": "City",
  "Rank": 85,
  "LocalizedName": "Ochlocknee",
  "EnglishName": "Ochlocknee",
  "PrimaryPostalCode": "31773",
  "Region": {
    "ID": "NAM",
    "LocalizedName": "North America",
    "EnglishName": "North America"
  },
  "Country": {
    "ID": "US",
    "LocalizedName": "United States",
    "EnglishName": "United States"
  },
  "AdministrativeArea": {
    "ID": "GA",
    "LocalizedName": "Georgia",
    "EnglishName": "Georgia",
    "Level": 1,
    "LocalizedType": "State",
    "EnglishType": "State",
    "CountryID": "US"
  },
  "TimeZone": {
    "Code": "EDT",
    "Name": "America/New_York",
    "GmtOffset": -4,
    "IsDaylightSaving": true,
    "NextOffsetChange": "2025-11-02T06:00:00Z"
  },
  "GeoPosition": {
    "Latitude": 30.974,
    "Longitude": -84.053,
    "Elevation": {
      "Metric": {
        "Value": 92,
        "Unit": "m",
        "UnitType": 5
      },
      "Imperial": {
        "Value": 301,
        "Unit": "ft",
        "UnitType": 0
      }
    }
  },
  "IsAlias": false,
  "SupplementalAdminAreas": [
    {
      "Level": 2,
      "LocalizedName": "Thomas",
      "EnglishName": "Thomas"
    }
  ],
  "DataSets": [
    "AirQualityCurrentConditions",
    "AirQualityForecasts",
    "Alerts",
    "DailyAirQualityForecast",
    "DailyPollenForecast",
    "ForecastConfidence",
    "FutureRadar",
    "MinuteCast",
    "ProximityNotification-Lightning",
    "Radar"
  ]
}

***** WEATHER *****

"""


def gather_location(lat: float, lon: float) -> Dict[str, Any]:

    my_keys = collect_keys()
    apikey = my_keys["Weather"]["accu-weather"]
    url = f"https://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={apikey}&q={lat}%2C{lon}"
    response = requests.get(url)
    data = cast(Dict[str, Any], response.json())
    return data


def gather_accuwx(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from Accuweather

    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return data: Weather data from Accuweather API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["accu-weather"]
    # Collect location
    location = gather_location(lat, lon)
    # url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={apikey}&units=metric"
    # response = requests.get(url)
    # data = cast(Dict[str, Any], response.json())
    # return data
    return location
