import requests
import pandas as pd
from typing import Dict, Any, cast, List
from raven.core.api_base import collect_keys
import openmeteo_requests  # type: ignore
import requests_cache
from retry_requests import retry  # type: ignore


def collect_weather(site: str, lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from the specified provider

    :param site: Weather provider to use
    :param lat: Latitude of the location
    :param lon: Longitude of the location

    :return: Weather data from the specified provider
    """
    # Call appropriate provider
    if site == "tmrwio":
        wx_data = collect_tomorrow(lat, lon)
    elif site == "openwx":
        wx_data = collect_openwx(lat, lon)
    elif site == "openmt":
        wx_data = collect_openmt(lat, lon)
    else:
        wx_data = {}
    return wx_data


def collect_tomorrow(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from Tomorrow.io

    :param apikey: API key for Tomorrow.io
    :return: Weather data from Tomorrow.io API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["tomorrow-io"]
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={apikey}"
    response = requests.get(url)
    return cast(Dict[str, Any], response.json())


def collect_openwx(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from OpenWeather

    :return: Weather data from OpenWeather API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["open-weather"]
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}"
    response = requests.get(url)
    return cast(Dict[str, Any], response.json())


def collect_openmt(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from Open-Meteo

    :return: Weather data from Tomorrow.io API
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "rain",
            "showers",
            "snowfall",
            "weather_code",
            "cloud_cover",
            "pressure_msl",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
        ],
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    wx_data = {
        "temperature": current.Variables(0).Value(),
        "relative_humidity": current.Variables(1).Value(),
        "apparent_temperature": current.Variables(2).Value(),
        "is_day": current.Variables(3).Value(),
        "precipitation": current.Variables(4).Value(),
        "rain": current.Variables(5).Value(),
        "showers": current.Variables(6).Value(),
        "snowfall": current.Variables(7).Value(),
        "wx_code": current.Variables(8).Value(),
        "cloud_cover": current.Variables(9).Value(),
        "pressure_msl": current.Variables(10).Value(),
        "surface_pressure": current.Variables(11).Value(),
        "wind_speed_10m": current.Variables(12).Value(),
        "wind_direction_10m": current.Variables(13).Value(),
        "wind_gusts_10m": current.Variables(14).Value(),
    }
    return wx_data
