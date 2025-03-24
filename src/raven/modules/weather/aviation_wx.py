import datetime
import json
from typing import Dict, Any, cast

import openmeteo_requests  # type: ignore
import requests
from raven.core.api_base import collect_keys
from pandas import DataFrame
from retry_requests import retry

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


# def gather_aviation_wx(station_id: str) -> Dict[str, Any]:
#    """
#    Collects weather data from Tomorrow.io
#
#    :param station_id: ICAO code of the station
#    :return data: Weather data from Tomorrow.io API
#    """


# Build time window; start time is one hour prior to current time, end time is current time
start_stamp = datetime.datetime.now() - datetime.timedelta(hours=1)
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
print(start_string)
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
print(end_string)

## Build current start time into datetime string
# start_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
## Start hour should be one hour prior to current
# start_hour = datetime.datetime.now().hour - 1
# end_hour = datetime.datetime.now().hour
# start_minute = datetime.datetime.now().minute
# start_second = datetime.datetime.now().second
## Build datetime strings for URL


# url = f"https://aviationweather.gov/api/data/dataserver?requestType=retrieve&dataSource=metars&stationString={station_id}&startTime=2025-03-24T00%3A00%3A00Z&endTime=2025-03-24T01%3A00%3A00Z&format=xml&mostRecent=true"
# response = requests.get(url)
# data = cast(Dict[str, Any], response.json())
# return data
