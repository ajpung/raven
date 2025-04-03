import json
from datetime import datetime
from typing import Dict, Any

from meteostat import Hourly  # type: ignore
from meteostat import Point

from raven.core.date_time import datetime_window

"""
`station` - The Meteostat ID of the weather station (only if query refers to multiple stations)	String
`time` - Observation datetime
`temp` - Air temperature [°C]
`dwpt` - Dew point [°C]
`rhum` - Relative humidity [%]
`prcp` - One-hour precipitation total [mm]
`snow` - Snow depth [mm]
`wdir` - Average wind direction [°]
`wspd` - Average wind speed [km/h]
`wpgt` - Peak wind gust in [km/h]
`pres` - Average sea-level air pressure [hPa]
`tsun` - One-hour total sunshine [m]
`coco` - Weather condition code
"""


def gather_meteostat(lat: float, lon: float, alt: float = 0) -> Dict[str, Any]:
    """
    Collects weather data from Meteo-stat

    :param station_id: ICAO code of the station
    :return data: Weather data from Meteo-stat API
    """
    # Define weather location
    location = Point(lat, lon, alt)

    # Set time period (current)
    current, early = datetime_window()
    start = datetime(current.year, current.month, current.day, current.hour - 1)
    end = start

    # Get hourly data
    data = Hourly(location, start, end)
    data = data.fetch()
    data["lat"] = lat
    data["lon"] = lon
    data["alt"] = alt
    return data  # type: ignore


def correct_meteostat(data: Dict[str, Any]) -> tuple[dict[str, Any], str, str, int]:
    """
    Corrects the data from Meteostat (units, date/time)
    :param data: Weather data from Aviation Weather API
    :return: Corrected weather data
    """
    # Capture date/time
    time_format = "%Y-%m-%d %H:%M:%S"
    dt_val = data["time"]
    date = datetime.strptime(dt_val, time_format).date().strftime("%Y-%m-%d")
    time = datetime.strptime(dt_val, time_format).time().strftime("%H:%M:%S")
    utc_epoch = int(datetime.strptime(dt_val, time_format).timestamp())
    return data, date, time, utc_epoch


def fill_meteostat(
    data: dict[str, Any],
    date: str,
    time: str,
    utc_epoch: int,
    json_file: str = "../docs/_static/json_template.json",
) -> dict:
    """
    Fills the JSON template with weather data from Meteostat
    :param data: Weather data from Meteostat API
    :param date: Date in API request
    :param time: Time in API request
    :param utc_epoch: Epoch time in API request
    :param json_file: JSON template file
    :return: JSON template filled with data from Meteostat
    """

    # ----- Read / fill JSON template -----
    avwx_dict = json.load(open(json_file))
    # Datetime
    avwx_dict["datetime"]["date"] = date
    avwx_dict["datetime"]["time"] = time
    avwx_dict["datetime"]["epoch"] = utc_epoch
    # Location
    avwx_dict["location"]["latitutde"] = data["lat"]
    avwx_dict["location"]["longitutde"] = data["lon"]
    avwx_dict["location"]["altitude"] = data["alt"]
    # Temp
    avwx_dict["data"]["temperature"]["measured"] = data["temp"]
    avwx_dict["data"]["temperature"]["dewpoint"] = data["dwpt"]
    # Relative humidity
    avwx_dict["data"]["temperature"]["humidity"] = data["rhum"]
    # Precipitation
    avwx_dict["data"]["precipitation"]["rain"]["accumulated"] = data["prcp"]
    avwx_dict["data"]["precipitation"]["snow"]["accumulated"] = data["snow"]
    # Pressure
    avwx_dict["data"]["pressure"]["sea_level"] = data["pres"]
    # Weather code
    avwx_dict["data"]["code"] = data["coco"]
    # Wind
    avwx_dict["data"]["wind"]["direction"]["heights"] = [0]
    avwx_dict["data"]["wind"]["direction"]["values"] = [data["wdir"]]
    avwx_dict["data"]["wind"]["gust"]["heights"] = [0]
    avwx_dict["data"]["wind"]["gust"]["values"] = [data["wpgt"]]
    avwx_dict["data"]["wind"]["speed"]["heights"] = [0]
    avwx_dict["data"]["wind"]["speed"]["values"] = [data["wspd"]]

    return avwx_dict  # type: ignore
