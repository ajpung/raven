import datetime
import json
import re
from typing import Dict, Any, Tuple

import openmeteo_requests  # type: ignore
import requests
import xmltodict

"""
Units taken from https://aviationweather.gov/data/api/#/Dataserver/dataserverMetars

__Clouds__
Altitude: km
Cover: %

__Temp__
Dewpoint: C
Temp: C
Apparent: C

__Health__
Concern: 0 - 5
Pollute: 0 - 5 (0:PM2.5, 1:PM10, 2:O3, 3:NO2, 4:CO, 5:SO2)
FireIdx: FWI
GrassIdx: 0 - 5 (0:None, 1:Very Low, 2:Low, 3:Medium, 4:High, 5:Very High) 
mepConcern: 0 - 5 (0:Good, 1:Moderate, 2:Unhealthy for Sensitive Groups, 3:Unhealthy, 4:Very Unhealthy, 5:Hazardous)
mepIndex: 0 - 5 (0:PM2.5, 1:PM10, 2:O3, 3:NO2, 4:CO, 5:SO2)

__Precip__
Hail predict: binary
Humidity: %
Ice accum: mm
Intensity: mm/hr
Prob: %
Type: 0 - 4 (0:N/A, 1:Rain, 2:Snow, 3:Freezing Rain, 4:Ice Pellets)

__Moon__
Phase: 0 - 7 (0:New, 1:Waxing Crescent, 2:First Quarter, 3:Waxing Gibbous, 4:Full, 5:Waning Gibbous, 6:Third Quarter, 7:Waning Crescent)

__Particulate__
Matter10: μg/m^3
Matter25: μg/m^3
pollutant: ppb (CO, NO2, O3, SO2)

__Pressure__
Sea Level: hPa
Surface Level: hPa

__Swells__
(Primary & Secondary)
Direction: degrees
Mean Period: seconds
Significant Height: m

__Soil__
Moisture (Volumetric): %
Temperature: C
    
__Solar__
DIF: W/m^2
DIR: W/m^2
GHI: W/m^2

__Snow__
Accumulation: mm

__Trees__
treeAcacia: 0 - 5 (0:None, 1:Very Low, 2:Low, 3:Medium, 4:High, 5:Very High)
treeAsh: "
treeBeech: "
treeBirch: "
treeCedar: "
treeCottonwood: "
treeCypress: "
treeElder: "
treeElm: "
treeHemlock: "
treeHickory: "
treeIndex: "
treeJuniper: "
treeMahogany: "
treeMaple: "
treeMulberry: "
treeOak: "
treePine: "
treeSpruce: "
treeSycamore: "
treeWalnut: "
treeWillow: "

__Visibility__
visibility: km

__Weeds__
weedGrassIndex: 0 - 5 (0:None, 1:Very Low, 2:Low, 3:Medium, 4:High, 5:Very High)
WeedIndex: 0 - 5 (0:None, 1:Very Low, 2:Low, 3:Medium, 4:High, 5:Very High)

__Waves__
SignificantHeight: m
Direction: degrees
MeanPeriod: seconds

__Wind__
Speed: m/s
Gust: m/s
Direction: degrees
windWaveSignificantHeight: m
windWaveDirection: degrees
windWaveMeanPeriod: seconds
"""


def create_time_window() -> Tuple[str, str]:
    """
    Creates a time window for the Aviation Wx API

    :return: Tuple of start and end time strings
    """
    # Build time window; start time is one hour prior to current time, end time is current time
    start_stamp = datetime.datetime.now() - datetime.timedelta(hours=1)

    # Build start time string
    start_date = start_stamp.strftime("%Y-%m-%d")
    start_hour = start_stamp.hour
    if start_hour < 10:
        start_hour = "0" + str(start_hour)  # type: ignore
    else:
        start_hour = str(start_hour)  # type: ignore
    start_minute = start_stamp.minute
    if start_minute < 10:
        start_minute = "0" + str(start_minute)  # type: ignore
    else:
        start_minute = str(start_minute)  # type: ignore
    start_second = start_stamp.second
    if start_second < 10:
        start_second = "0" + str(start_second)  # type: ignore
    else:
        start_second = str(start_second)  # type: ignore
    start_string = (
        start_date + "T" + start_hour + "%3A" + start_minute + "%3A" + start_second + "Z"  # type: ignore
    )

    # Build end time string
    end_stamp = datetime.datetime.now()
    end_date = end_stamp.strftime("%Y-%m-%d")
    end_hour = end_stamp.hour
    if end_hour < 10:
        end_hour = "0" + str(end_hour)  # type: ignore
    else:
        end_hour = str(end_hour)  # type: ignore
    end_minute = end_stamp.minute
    if end_minute < 10:
        end_minute = "0" + str(end_minute)  # type: ignore
    else:
        end_minute = str(end_minute)  # type: ignore
    end_second = end_stamp.second
    if end_second < 10:
        end_second = "0" + str(end_second)  # type: ignore
    else:
        end_second = str(end_second)  # type: ignore
    end_string = end_date + "T" + end_hour + "%3A" + end_minute + "%3A" + end_second + "Z"  # type: ignore

    return start_string, end_string


def gather_aviation_wx(station_id: str) -> Dict[str, Any]:
    """
    Collects weather data from Tomorrow.io

    :param station_id: ICAO code of the station
    :return data: Weather data from Tomorrow.io API
    """
    # Get time window
    start_string, end_string = create_time_window()

    # Create query URL
    url = f"https://aviationweather.gov/api/data/dataserver?requestType=retrieve&dataSource=metars&stationString={station_id}&startTime={start_string}&endTime={end_string}&format=xml&mostRecent=true"
    response = requests.get(url)

    # Parse the XML string to a dictionary
    data = xmltodict.parse(response.text)
    # data = json.dumps(data, indent=4)  # type: ignore
    return data


def correct_aviation(data: Dict[str, Any]) -> tuple[dict[str, Any], str, str, int]:
    """
    Corrects the data from Aviation Weather (units, date/time)
    :param data: Weather data from Aviation Weather API
    :return: Corrected weather data
    """
    # Windspeed (kts -> km/hr)
    data["response"]["data"]["METAR"]["wind_speed_kph"] = (
        float(data["response"]["data"]["METAR"]["wind_speed_kt"]) * 1.852
    )
    # Visibility (statue miles -> km)
    vis = data["response"]["data"]["METAR"]["visibility_statute_mi"]
    vis = re.sub("[^A-Za-z0-9]+", "", vis)
    data["response"]["data"]["METAR"]["visibility_km"] = float(vis) * 1.60934

    # Apply Unit Corrections
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    dt_val = data["response"]["data"]["METAR"]["observation_time"]
    date = datetime.datetime.strptime(dt_val, time_format).date().strftime("%Y-%m-%d")
    time = datetime.datetime.strptime(dt_val, time_format).time().strftime("%H:%M:%S")
    utc_epoch = int(datetime.datetime.strptime(dt_val, time_format).timestamp())
    return data, date, time, utc_epoch


def fill_aviation(
    data: dict[str, Any],
    date: str,
    time: str,
    utc_epoch: int,
    json_file: str = "../docs/_static/json_template.json",
) -> dict:
    """
    Fills the JSON template with METAR data from Aviatoin Weather
    :param data: Weather data from Aviation Weather API
    :param date: Date in API request
    :param time: Time in API request
    :param utc_epoch: Epoch time in API request
    :param json_file: JSON template file
    :return: JSON template filled with data from Tomorrow.io
    """
    # ----- Read / fill JSON template -----
    avwx_dict = json.load(open(json_file))
    # Datetime
    avwx_dict["datetime"]["date"] = date
    avwx_dict["datetime"]["time"] = time
    avwx_dict["datetime"]["epoch"] = utc_epoch
    # Location
    avwx_dict["location"]["latitutde"] = data["response"]["data"]["METAR"]["latitude"]
    avwx_dict["location"]["longitutde"] = data["response"]["data"]["METAR"]["longitude"]
    # Clouds
    cc = data["response"]["data"]["METAR"]["sky_condition"]["@sky_cover"]
    if cc == "SKC":
        cover = 0.0
    elif cc == "NSC":
        cover = 6.0
    elif cc == "FEW":
        cover = 25.0
    elif cc == "SCT":
        cover = 50.0
    elif cc == "BKN":
        cover = 75.0
    elif cc == "OVC":
        cover = 100
    elif cc == "CAVOK":
        cover = 0.0
    else:
        cover = 999
    avwx_dict["data"]["clouds"]["cover"] = cover
    # Temp
    avwx_dict["data"]["temperature"]["measured"] = data["response"]["data"]["METAR"][
        "temp_c"
    ]
    avwx_dict["data"]["temperature"]["dewpoint"] = data["response"]["data"]["METAR"][
        "dewpoint_c"
    ]
    # Visibility
    avwx_dict["data"]["visibility"] = data["response"]["data"]["METAR"]["visibility_km"]
    # Weather code
    if "wx_string" in data["response"]["data"]["METAR"]:
        avwx_dict["data"]["code"] = data["response"]["data"]["METAR"]["wx_string"]
    # Wind
    avwx_dict["data"]["wind"]["direction"] = data["response"]["data"]["METAR"][
        "wind_dir_degrees"
    ]
    avwx_dict["data"]["wind"]["speed"] = data["response"]["data"]["METAR"][
        "wind_speed_kph"
    ]
    return avwx_dict  # type: ignore


def collect_aviationwx(station_id: str) -> Dict[str, Any]:
    """
    Collects, corrects, and formats weather data from Tomorrow.io
    :param station_id: ICAO code of the station
    :return avia_dict: Weather data from Tomorrow.io API
    """
    # Collect data from API
    data = gather_aviation_wx(station_id)
    # Correct data
    data, date, time, utc_epoch = correct_aviation(data)
    # Fill JSON template
    avia_dict = fill_aviation(data, date, time, utc_epoch)
    return avia_dict
