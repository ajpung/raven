import requests
from typing import Dict, Any, cast
from raven.core.api_base import collect_keys


def collect_weather(provider: str) -> Dict[str, Any]:
    """
    Collects weather data from the specified provider
    :param provider: Weather data provider
    :return: Weather data from the specified provider
    """
    keys = collect_keys()
    if provider == "Tomorrow-io":
        data = collect_tomorrow(keys["Tomorrow-io"])
    else:
        raise ValueError(f"Provider {provider} is not supported")
    return data


def collect_tomorrow(apikey: str) -> Dict[str, Any]:
    """
    Collects weather data from Tomorrow.io

    :param apikey: API key for Tomorrow.io
    :return: Weather data from Tomorrow.io API
    """
    url = (
        f"https://api.tomorrow.io/v4/weather/realtime?location=toronto&apikey={apikey}"
    )
    response = requests.get(url)
    return cast(Dict[str, Any], response.json())


def collect_openwx(apikey: str, lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from Tomorrow.io

    :param apikey: API key for Tomorrow.io
    :return: Weather data from Tomorrow.io API
    """
    url = (
        f"https://api.tomorrow.io/v4/weather/realtime?location=toronto&apikey={apikey}"
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat} & lon={lon} & appid={apikey}"
    )
    response = requests.get(url)
    return cast(Dict[str, Any], response.json())
