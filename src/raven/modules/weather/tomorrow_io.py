from typing import Dict, Any, cast

import openmeteo_requests  # type: ignore
import requests
from retry_requests import retry  # type: ignore

from raven.core.api_base import collect_keys

"""
Inherent units:
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
    return cast(Dict[str, Any], response.json())
