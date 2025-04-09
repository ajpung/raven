import datetime
import json
from typing import Dict, Any, cast

import openmeteo_requests  # type: ignore
import requests
from raven.core.api_base import collect_keys
from pandas import DataFrame
from retry_requests import retry

"""
The Weather and Marine APIs provide slightly different weather data. For
now, the Sports API returns empty fields and the Astronomy API data are
also included in the Marine data -- neither of these are used. Furthermore,
Marine data is daily, while the weather data are current; for a similar
reason, the Marine data are also not used, but listed here for reference.

Units taken from:
    (api example) https://www.weatherapi.com/api-explorer.aspx
    (weather) https://www.weatherapi.com/docs/

# Weather data
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

# Marine data
{
    "location":{
        "name":"Long Run",
        "region":"Kentucky",
        "country":"United States of America",
        "lat":38.232,
        "lon":-85.424,
        "tz_id":"America/Kentucky/Louisville",
        "localtime_epoch":1744195256,
        "localtime":"2025-04-09 06:40"
    },
    "forecast":{
        "forecastday":[
            {
                "date":"2025-04-09",
                "date_epoch":1744156800,
                "day":{
                    "maxtemp_c":6.7,
                    "maxtemp_f":44.1,
                    "mintemp_c":1.5,
                    "mintemp_f":34.7,
                    "avgtemp_c":4.3,
                    "avgtemp_f":39.8,
                    "maxwind_mph":10.5,
                    "maxwind_kph":16.8,
                    "totalprecip_mm":0.0,
                    "totalprecip_in":0.0,
                    "totalsnow_cm":0.0,
                    "avgvis_km":10.0,
                    "avgvis_miles":6.0,
                    "avghumidity":47.0,
                    "condition":{
                        "text":"Partly Cloudy ",
                        "icon":"//cdn.weatherapi.com/weather/64x64/day/116.png",
                        "code":1003
                    },
                    "uv":2.0
                },
                "astro":{
                    "sunrise":"06:42 AM",
                    "sunset":"07:41 PM",
                    "moonrise":"04:45 PM",
                    "moonset":"05:16 AM",
                    "moon_phase":
                    "Waxing Gibbous",
                    "moon_illumination":80,
                    "is_moon_up":0,
                    "is_sun_up":0
                }
            }
        ]
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
    # url = https://api.weatherapi.com/v1/current.json?key={apikey}&q=31.5/-51.3&aqi=yes
    # Marine
    # url = https://api.weatherapi.com/v1/marine.json?key={apikey}&q=31.5/-51.3&days=1
    # Astronomy
    # url = https://api.weatherapi.com/v1/astronomy.json?key={apikey}&q=31.5/-51.3&dt=2025-04-08
    # Sports
    # url = https://api.weatherapi.com/v1/sports.json?key={apikey}&q=31.5/-51.3

    url = f"https://api.weatherapi.com/v1/current.json?key={apikey}&q={lat},{lon}&aqi=yes&alerts=yes&tides=yes&solar=yes&et0=yes"
    response = requests.get(url)
    data = cast(Dict[str, Any], response.json())
    return data


def correct_weatherapi(data: Dict[str, Any]) -> tuple[dict[str, Any], str, str, int]:
    """
    Corrects the data from WeatherAPI (units, date/time)
    :param data: Weather data from WeatherAPI
    :return: Corrected weather data
    """
    # Convert datetime to epoch using DateTime
    time_format = "%Y-%m-%d %H:%M"
    date = (
        datetime.datetime.strptime(data["current"]["last_updated"], time_format)
        .date()
        .strftime("%Y-%m-%d")
    )
    time = (
        datetime.datetime.strptime(data["current"]["last_updated"], time_format)
        .time()
        .strftime("%H:%M")
    )
    utc_epoch = int(data["current"]["last_updated_epoch"])
    return data, date, time, utc_epoch


def fill_weatherapi(
    data: dict[str, Any],
    date: str,
    time: str,
    utc_epoch: int,
    json_file: str = "../docs/_static/json_template.json",
) -> dict:
    """
    Fills the JSON template with the data from WeatherAPI
    :param data: Weather data from WeatherAPI
    :param date: Date in API request
    :param time: Time in API request
    :param utc_epoch: Epoch time in API request
    :param json_file: JSON template file
    :return: JSON template filled with data from WeatherAPI
    """

    # ----- Read / fill JSON template -----
    wxapi_dict = json.load(open(json_file))
    # Datetime
    wxapi_dict["datetime"]["date"] = date
    wxapi_dict["datetime"]["time"] = time
    wxapi_dict["datetime"]["epoch"] = utc_epoch
    # Location
    wxapi_dict["location"]["latitutde"] = data["location"]["lat"]
    wxapi_dict["location"]["longitutde"] = data["location"]["lon"]
    # Clouds
    wxapi_dict["data"]["clouds"]["cover"] = data["current"]["cloud"]
    # Temp
    wxapi_dict["data"]["temperature"]["dewpoint"] = data["current"]["dewpoint_c"]
    wxapi_dict["data"]["temperature"]["humidity"] = data["current"]["humidity"]
    wxapi_dict["data"]["temperature"]["measured"] = data["current"]["temp_c"]
    wxapi_dict["data"]["temperature"]["apparent"] = data["current"]["feelslike_c"]
    # Precipitation
    wxapi_dict["data"]["precipitation"]["rain"]["accumulated"] = data["current"][
        "precip_mm"
    ]
    # Pressure
    wxapi_dict["data"]["pressure"]["sea_level"] = data["current"]["pressure_mb"]
    # Health
    wxapi_dict["data"]["health"]["uv_index"] = data["current"]["uv"]
    # Visibility
    wxapi_dict["data"]["visibility"] = data["current"]["vis_km"]
    # Weather code
    wxapi_dict["data"]["condition"]["code"] = data["current"]["condition"]["code"]
    wxapi_dict["data"]["condition"]["text"] = data["current"]["condition"]["text"]
    # Wind
    wxapi_dict["data"]["wind"]["direction"] = data["current"]["wind_degree"]
    wxapi_dict["data"]["wind"]["gust"] = data["current"]["gust_kph"]
    wxapi_dict["data"]["wind"]["speed"] = data["current"]["wind_kph"]
    return wxapi_dict  # type: ignore


def collect_weatherapi(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects, corrects, and formats weather data from Tomorrow.io
    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return tmrw_dict: Weather data from Tomorrow.io API
    """
    # Collect data from API
    data = gather_weatherapi(lat, lon)
    # Correct data
    data, date, time, utc_epoch = correct_weatherapi(data)
    # Fill JSON template
    wxapi_dict = fill_weatherapi(data, date, time, utc_epoch)
    return wxapi_dict
