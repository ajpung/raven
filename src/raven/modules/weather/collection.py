from typing import Any, Collection
import openmeteo_requests  # type: ignore
from retry_requests import retry  # type: ignore

from raven.modules.weather.tomorrow_io import collect_tomorrow
from raven.modules.weather.open_meteo import gather_openmeteo
from raven.modules.weather.visual_crossing import gather_visualcrossing


def collect_weather(lat: float, lon: float) -> list[Collection[str | float | Any]]:
    """
    Collects weather data from the specified provider
    :param lat: Latitude of the location
    :param lon: Longitude of the location

    :return: Weather data from the specified provider
    """
    # Call appropriate provider
    wx_data0 = collect_tomorrow(lat, lon)
    wx_data2 = gather_openmeteo(lat, lon)
    return [wx_data0, wx_data2]
