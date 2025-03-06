from typing import Dict, Any, cast
import json
import openmeteo_requests  # type: ignore
import requests
from retry_requests import retry  # type: ignore

from raven.core.api_base import collect_keys

"""
'queryCost': 1
'latitude':  degrees
'longitude': degrees
'resolvedAddress': degrees, degrees
'address': degrees, degrees
'timezone': Country/State/City
'tzoffset': hours
'currentConditions': {
    'datetime': HH:MM:SS
    'datetimeEpoch': seconds
    'temp': C
    'feelslike': C
    'humidity': %
    'dew': C
    'precip': mm
    'precipprob': %
    'snow': cm
    'snowdepth': cm
    'preciptype': None
    'windgust': km/h
    'windspeed': km/h
    'winddir': degrees
    'pressure': hPa
    'visibility': km
    'cloudcover': %
    'solarradiation': W/m2
    'solarenergy': MJ/m2
    'uvindex': 1.0
    'conditions': 'Clear'
    'icon': 'clear-day'
    'sunrise': HH:MM:SS
    'sunriseEpoch': seconds
    'sunset': HH:MM:SS
    'sunsetEpoch': seconds
    'moonphase': normalized fraction
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
        "contentType": "json",
        "elements": "datetime,datetimeEpoch,temp,humidity,dew,precip,snow,snowdepth,windgust,windspeed,winddir,pressure,visibility,cloudcover,solarradiation,solarenergy,uvindex,conditions,icon,sunriseEpoch,sunsetEpoch,moonriseEpoch,moonsetEpoch,moonphase,cape,cin",
        "include": "current",
        "key": apikey,
        "maxStations": 0,
        "source": "stats",
        "timezone": "Z",
        "unitGroup": "metric",
    }
    response = requests.get(url, params=params)
    return cast(Dict[str, Any], response.json())


def correct_visualcrossing(
    data: Dict[str, Any],
) -> tuple[dict[str, Any], str, str, int]:
    """
    Corrects the data from Visual Crossing (units, date/time)
    :param data: Weather data from Visual Crossing API
    :return: Corrected weather data
    """
    # Apply Unit Corrections
    #   (snow mm->cm)
    data["currentConditions"]["snow"] *= 10
    #   (snow depth cm->m)
    data["currentConditions"]["snowdepth"] /= 10

    # Convert epoch to date and time strings
    from datetime import datetime

    dt = datetime.fromtimestamp(data["currentConditions"]["datetimeEpoch"])
    date = dt.strftime("%Y-%m-%d")
    time = dt.strftime("%H:%M:%S")
    utc_epoch = data["currentConditions"]["datetimeEpoch"]
    return data, date, time, utc_epoch


def fill_visualcrossing(
    data, date, time, utc_epoch, json_file: str = "../docs/_static/json_template.json"
):
    """
    Fills the JSON template with the data from Visual Crossing
    :param data: Weather data from Visual Crossing API
    :param date: Date in API request
    :param time: Time in API request
    :param utc_epoch: Epoch time in API request
    :param json_file: JSON template file
    :return: JSON template filled with data from Tomorrow.io
    """
    # ----- Read / fill JSON template -----
    viscross_dict = json.load(open(json_file))
    # Datetime
    viscross_dict["datetime"]["date"] = date
    viscross_dict["datetime"]["time"] = time
    viscross_dict["datetime"]["epoch"] = utc_epoch
    # Location
    viscross_dict["location"]["latitude"] = data["currentConditions"]["latitude"]
    viscross_dict["location"]["longitude"] = data["currentConditions"]["longitude"]
    # Clouds
    viscross_dict["data"]["clouds"]["cover"] = data["currentConditions"]["cloudcover"]
    # Energy
    viscross_dict["data"]["energy"]["conv_avail_pot"] = data["currentConditions"][
        "cape"
    ]
    viscross_dict["data"]["energy"]["conv_inhibition"] = data["currentConditions"][
        "cin"
    ]
    # Health
    viscross_dict["data"]["health"]["uvindex"] = data["currentConditions"]["uvindex"]
    # Moon
    viscross_dict["data"]["moon"]["phase"] = data["currentConditions"]["moonphase"]
    viscross_dict["data"]["moon"]["moonrise"] = data["currentConditions"][
        "moonriseEpoch"
    ]
    viscross_dict["data"]["moon"]["moonset"] = data["currentConditions"]["moonsetEpoch"]
    # Precipitation
    viscross_dict["data"]["precipitation"]["rain"] = data["currentConditions"]["precip"]
    viscross_dict["data"]["precipitation"]["probability"] = data["currentConditions"][
        "precipprob"
    ]
    # Snow
    viscross_dict["data"]["snow"]["intensity"] = data["currentConditions"]["snow"]
    viscross_dict["data"]["snow"]["accumulated"] = data["currentConditions"][
        "snowdepth"
    ]
    # Pressure
    viscross_dict["data"]["pressure"]["sea_level"] = data["currentConditions"][
        "pressure"
    ]
    # Radiation
    viscross_dict["data"]["radiation"]["cape"] = data["currentConditions"]["cape"]
    viscross_dict["data"]["radiation"]["convective_inhibition"] = data[
        "currentConditions"
    ]["cin"]
    viscross_dict["data"]["radiation"]["direct"] = data["currentConditions"][
        "solarradiation"
    ]
    # Sun
    viscross_dict["data"]["sun"]["sunrise"] = data["currentConditions"]["sunriseEpoch"]
    viscross_dict["data"]["sun"]["sunset"] = data["currentConditions"]["sunsetEpoch"]
    # Temperature
    viscross_dict["data"]["temperature"]["measured"] = data["currentConditions"]["temp"]
    viscross_dict["data"]["temperature"]["apparent"] = data["currentConditions"][
        "feelslike"
    ]
    viscross_dict["data"]["temperature"]["dewpoint"] = data["currentConditions"]["dew"]
    viscross_dict["data"]["temperature"]["humidity"] = data["currentConditions"][
        "humidity"
    ]
    # Visibility
    viscross_dict["data"]["visibility"]["distance"] = data["currentConditions"][
        "visibility"
    ]
    # Wind
    viscross_dict["data"]["wind"]["speed"]["heights"] = [0]
    viscross_dict["data"]["wind"]["speed"]["values"] = [
        data["currentConditions"]["windspeed"]
    ]
    viscross_dict["data"]["wind"]["gust"]["heights"] = [0]
    viscross_dict["data"]["wind"]["gust"]["values"] = [
        data["currentConditions"]["windgust"]
    ]
    viscross_dict["data"]["wind"]["direction"]["heights"] = [0]
    viscross_dict["data"]["wind"]["direction"]["values"] = [
        data["currentConditions"]["winddir"]
    ]
    return viscross_dict


def collect_visualcrossing(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects, corrects, and formats weather data from Visual Crossing
    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return tmrw_dict: Weather data from Visual Crossing API
    """
    # Collect data from API
    data = gather_visualcrossing(lat, lon)
    # Correct data
    data, date, time, utc_epoch = correct_visualcrossing(data)
    # Fill JSON template
    vscrs_dict = fill_visualcrossing(data, date, time, utc_epoch)
    return vscrs_dict
