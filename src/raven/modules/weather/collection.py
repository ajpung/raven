import requests
from typing import Dict, Any, cast, List
from raven.core.api_base import collect_keys


def collect_weather(lat: float, lon: float) -> List[Dict[str, Any]]:
    """
    Collects weather data from the specified provider
    :param provider: Weather data provider
    :return: Weather data from the specified provider
    """
    tmrw_data = collect_tomorrow(lat, lon)
    opwx_data = collect_openwx(lat, lon)
    return [tmrw_data, opwx_data]


def collect_tomorrow(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from Tomorrow.io

    :param apikey: API key for Tomorrow.io
    :return: Weather data from Tomorrow.io API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["tomorrow-io"]
    url = (
        f"https://api.tomorrow.io/v4/weather/realtime?location=toronto&apikey={apikey}"
    )
    response = requests.get(url)
    return cast(Dict[str, Any], response.json())


def collect_openwx(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from Tomorrow.io

    :param apikey: API key for Tomorrow.io
    :return: Weather data from Tomorrow.io API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["open-weather"]
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}"
    response = requests.get(url)
    return cast(Dict[str, Any], response.json())
