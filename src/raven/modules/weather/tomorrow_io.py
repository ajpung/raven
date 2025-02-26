import datetime
import json
from typing import Dict, Any, cast

import openmeteo_requests  # type: ignore
import requests
from raven.core.api_base import collect_keys
from retry_requests import retry  # type: ignore

"""
Units taken from https://docs.tomorrow.io/reference/weather-data-layers#field-descriptors

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


def collect_tomorrow(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from Tomorrow.io

    :param apikey: API key for Tomorrow.io
    :return: Weather data from Tomorrow.io API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["tomorrow-io"]
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={apikey}&units=metric"
    response = requests.get(url)
    data = cast(Dict[str, Any], response.json())

    # Apply Unit Corrections
    # (snow)
    data["data"]["values"]["snowIntensity"] = (
        data["data"]["values"]["snowIntensity"] / 10
    )  # mm (ingest) > cm (expected)
    # (wind)
    data["data"]["values"]["windSpeed"] = (
        data["data"]["values"]["windSpeed"] * 3.6
    )  # m/s (ingest) > km/hr (expected)
    data["data"]["values"]["windGust"] = (
        data["data"]["values"]["windGust"] * 3.6
    )  # m/s (ingest) > km/hr (expected)

    # Convert datetime to epoch using DateTime
    date = (
        datetime.datetime.strptime(data["data"]["time"], "%Y-%m-%dT%H:%M:%SZ")
        .date()
        .strftime("%Y-%m-%d")
    )
    time = (
        datetime.datetime.strptime(data["data"]["time"], "%Y-%m-%dT%H:%M:%SZ")
        .time()
        .strftime("%H:%M:%S")
    )
    utc_epoch = int(
        datetime.datetime.strptime(
            data["data"]["time"], "%Y-%m-%dT%H:%M:%SZ"
        ).timestamp()
    )

    # TODO: Write datetime-to-epoch converter

    # ----- Read / fill JSON template -----
    tmrw_dict = json.load(open("../docs/_static/json_template.json"))
    # Datetime
    tmrw_dict["datetime"]["date"] = date
    tmrw_dict["datetime"]["time"] = time
    tmrw_dict["datetime"]["epoch"] = utc_epoch
    # Location
    tmrw_dict["location"]["latitutde"] = data["location"]["lat"]
    tmrw_dict["location"]["longitutde"] = data["location"]["lon"]
    # Clouds
    tmrw_dict["data"]["clouds"]["base"] = data["data"]["values"]["cloudBase"]
    tmrw_dict["data"]["clouds"]["ceiling"] = data["data"]["values"]["cloudCeiling"]
    tmrw_dict["data"]["clouds"]["cover"] = data["data"]["values"]["cloudCover"]
    # Temp
    tmrw_dict["data"]["temperature"]["dewpoint"] = data["data"]["values"]["dewPoint"]
    tmrw_dict["data"]["temperature"]["measured"] = data["data"]["values"]["temperature"]
    tmrw_dict["data"]["temperature"]["apparent"] = data["data"]["values"][
        "temperatureApparent"
    ]
    tmrw_dict["data"]["temperature"]["humidity"] = data["data"]["values"]["humidity"]
    # Precipitation
    tmrw_dict["data"]["precipitation"]["rain"]["frz_rain_int"] = data["data"]["values"][
        "freezingRainIntensity"
    ]
    tmrw_dict["data"]["precipitation"]["rain"]["intensity"] = data["data"]["values"][
        "rainIntensity"
    ]
    tmrw_dict["data"]["precipitation"]["hail"]["probability"] = data["data"]["values"][
        "hailProbability"
    ]
    tmrw_dict["data"]["precipitation"]["hail"]["size"] = data["data"]["values"][
        "hailSize"
    ]
    tmrw_dict["data"]["precipitation"]["sleet"]["intensity"] = data["data"]["values"][
        "sleetIntensity"
    ]
    tmrw_dict["data"]["precipitation"]["snow"]["intensity"] = data["data"]["values"][
        "snowIntensity"
    ]
    tmrw_dict["data"]["precipitation"]["probability"] = data["data"]["values"][
        "precipitationProbability"
    ]
    # Pressure
    tmrw_dict["data"]["pressure"]["sea_level"] = data["data"]["values"][
        "pressureSeaLevel"
    ]
    tmrw_dict["data"]["pressure"]["surface_level"] = data["data"]["values"][
        "pressureSurfaceLevel"
    ]
    # Health
    tmrw_dict["data"]["health"]["uv_concern"] = data["data"]["values"][
        "uvHealthConcern"
    ]
    tmrw_dict["data"]["health"]["uv_index"] = data["data"]["values"]["uvIndex"]
    # Visibility
    tmrw_dict["data"]["visibility"] = data["data"]["values"]["visibility"]
    # Weather code
    tmrw_dict["data"]["code"] = data["data"]["values"]["weatherCode"]
    # Wind
    tmrw_dict["data"]["wind"]["direction"] = data["data"]["values"]["windDirection"]
    tmrw_dict["data"]["wind"]["gust"] = data["data"]["values"]["windGust"]
    tmrw_dict["data"]["wind"]["speed"] = data["data"]["values"]["windSpeed"]
    return tmrw_dict
