from typing import Any, Dict, Tuple
import datetime
import openmeteo_requests  # type: ignore
import pandas as pd
from typing import Dict, Any, cast
import requests_cache
from retry_requests import retry  # type: ignore
from pandas import DataFrame

"""
Units taken from https://open-meteo.com/en/docs

__Clouds__
Cloud cover: 

__Energy__


__Health__
UV index


__Moon__
 

__Particulate__
 

__Precip__
Precip. Prob.: 
Precip: 
Rain: 
Showers:
Evapotranspiration: 
Vapor pressure deficit: 

__Pressure__
Sea Level:
Surface:

__Radiation__
"cape",
"lifted_index",
"convective_inhibition",
"shortwave_radiation_instant",
"direct_radiation_instant",
"diffuse_radiation_instant",
"direct_normal_irradiance_instant",
"global_tilted_irradiance_instant",
"terrestrial_radiation_instant",

__Soil__
Temperature:
Moisture:

__Solar__
Sun duration: 

__Snow__
Snowfall:
Snow depth:

__Swells__


__Temp__
Temperature:
Apparent temp:
Rel. humidity:
Dewpoint: 
Wet bulb temp:
Freezing level height:
Boundary layer height:

__Trees__


__Visibility__
Visibility:  

__Weeds__


__Waves__


__Wind__
Speed:
Direction:
Gusts:


"weather_code",
"is_day",
"total_column_integrated_water_vapour",
"temperature_30hPa",
"relative_humidity_30hPa",
"cloud_cover_30hPa",
"wind_speed_30hPa",
"wind_direction_30hPa",
"geopotential_height_30hPa",
"""


def gather_openmeteo(lat: float, lon: float):
    # NOTE:
    #   - Current conditions are based on 15-minutely weather model data
    #   - Every weather variable available in hourly data is available as current condition as well!

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Form URL
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "dew_point_2m",
            "apparent_temperature",
            "precipitation_probability",
            "precipitation",
            "rain",
            "showers",
            "snowfall",
            "snow_depth",
            "weather_code",
            "pressure_msl",
            "surface_pressure",
            "cloud_cover",
            "cloud_cover_low",
            "cloud_cover_mid",
            "cloud_cover_high",
            "visibility",
            "evapotranspiration",
            "et0_fao_evapotranspiration",
            "vapour_pressure_deficit",
            "wind_speed_10m",
            "wind_speed_80m",
            "wind_speed_120m",
            "wind_speed_180m",
            "wind_direction_10m",
            "wind_direction_80m",
            "wind_direction_120m",
            "wind_direction_180m",
            "wind_gusts_10m",
            "temperature_80m",
            "temperature_120m",
            "temperature_180m",
            "soil_temperature_0cm",
            "soil_temperature_6cm",
            "soil_temperature_18cm",
            "soil_temperature_54cm",
            "soil_moisture_0_to_1cm",
            "soil_moisture_1_to_3cm",
            "soil_moisture_3_to_9cm",
            "soil_moisture_9_to_27cm",
            "soil_moisture_27_to_81cm",
            "uv_index",
            "uv_index_clear_sky",
            "is_day",
            "sunshine_duration",
            "wet_bulb_temperature_2m",
            "total_column_integrated_water_vapour",
            "cape",
            "lifted_index",
            "convective_inhibition",
            "freezing_level_height",
            "boundary_layer_height",
            "shortwave_radiation",
            "direct_radiation",
            "diffuse_radiation",
            "direct_normal_irradiance",
            "global_tilted_irradiance",
            "terrestrial_radiation",
            "shortwave_radiation_instant",
            "direct_radiation_instant",
            "diffuse_radiation_instant",
            "direct_normal_irradiance_instant",
            "global_tilted_irradiance_instant",
            "terrestrial_radiation_instant",
            "temperature_1000hPa",
            "temperature_975hPa",
            "temperature_950hPa",
            "temperature_925hPa",
            "temperature_900hPa",
            "temperature_850hPa",
            "temperature_800hPa",
            "temperature_700hPa",
            "temperature_600hPa",
            "temperature_500hPa",
            "temperature_400hPa",
            "temperature_300hPa",
            "temperature_250hPa",
            "temperature_200hPa",
            "temperature_150hPa",
            "temperature_100hPa",
            "temperature_70hPa",
            "temperature_50hPa",
            "temperature_30hPa",
            "relative_humidity_1000hPa",
            "relative_humidity_975hPa",
            "relative_humidity_950hPa",
            "relative_humidity_925hPa",
            "relative_humidity_900hPa",
            "relative_humidity_850hPa",
            "relative_humidity_800hPa",
            "relative_humidity_700hPa",
            "relative_humidity_600hPa",
            "relative_humidity_500hPa",
            "relative_humidity_400hPa",
            "relative_humidity_300hPa",
            "relative_humidity_250hPa",
            "relative_humidity_200hPa",
            "relative_humidity_150hPa",
            "relative_humidity_100hPa",
            "relative_humidity_70hPa",
            "relative_humidity_50hPa",
            "relative_humidity_30hPa",
            "cloud_cover_1000hPa",
            "cloud_cover_975hPa",
            "cloud_cover_950hPa",
            "cloud_cover_925hPa",
            "cloud_cover_900hPa",
            "cloud_cover_850hPa",
            "cloud_cover_800hPa",
            "cloud_cover_700hPa",
            "cloud_cover_600hPa",
            "cloud_cover_500hPa",
            "cloud_cover_400hPa",
            "cloud_cover_300hPa",
            "cloud_cover_250hPa",
            "cloud_cover_200hPa",
            "cloud_cover_150hPa",
            "cloud_cover_100hPa",
            "cloud_cover_70hPa",
            "cloud_cover_50hPa",
            "cloud_cover_30hPa",
            "wind_speed_1000hPa",
            "wind_speed_975hPa",
            "wind_speed_950hPa",
            "wind_speed_925hPa",
            "wind_speed_900hPa",
            "wind_speed_850hPa",
            "wind_speed_800hPa",
            "wind_speed_700hPa",
            "wind_speed_600hPa",
            "wind_speed_500hPa",
            "wind_speed_400hPa",
            "wind_speed_300hPa",
            "wind_speed_250hPa",
            "wind_speed_200hPa",
            "wind_speed_150hPa",
            "wind_speed_100hPa",
            "wind_speed_70hPa",
            "wind_speed_50hPa",
            "wind_speed_30hPa",
            "wind_direction_1000hPa",
            "wind_direction_975hPa",
            "wind_direction_950hPa",
            "wind_direction_925hPa",
            "wind_direction_900hPa",
            "wind_direction_850hPa",
            "wind_direction_800hPa",
            "wind_direction_700hPa",
            "wind_direction_600hPa",
            "wind_direction_500hPa",
            "wind_direction_400hPa",
            "wind_direction_300hPa",
            "wind_direction_250hPa",
            "wind_direction_200hPa",
            "wind_direction_150hPa",
            "wind_direction_100hPa",
            "wind_direction_70hPa",
            "wind_direction_50hPa",
            "wind_direction_30hPa",
            "geopotential_height_1000hPa",
            "geopotential_height_975hPa",
            "geopotential_height_950hPa",
            "geopotential_height_925hPa",
            "geopotential_height_900hPa",
            "geopotential_height_850hPa",
            "geopotential_height_800hPa",
            "geopotential_height_700hPa",
            "geopotential_height_600hPa",
            "geopotential_height_500hPa",
            "geopotential_height_400hPa",
            "geopotential_height_300hPa",
            "geopotential_height_250hPa",
            "geopotential_height_200hPa",
            "geopotential_height_150hPa",
            "geopotential_height_100hPa",
            "geopotential_height_70hPa",
            "geopotential_height_50hPa",
            "geopotential_height_30hPa",
        ],
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    return response


def correct_openmeteo(data) -> tuple[dict[str, Any], str, str, int]:
    """
    Corrects the data from Tomorrow.io (units, date/time)
    :param data: Weather data from Tomorrow.io API
    :return: Corrected weather data
    """
    # Convert datetime to epoch using DateTime
    current = data.Current()
    ctime = current.Time()
    cur_dt = datetime.datetime.fromtimestamp(ctime)
    ddate = cur_dt.date().strftime("%Y-%m-%d")
    dtime = cur_dt.time().strftime("%H:%M:%S")

    # Extract LLA
    lat, lon, alt = data.Latitude(), data.Longitude(), data.Elevation()

    # Apply Unit Corrections

    return data, ddate, dtime, ctime
    # return


lat, lon = 15.0, -108.5
data = gather_openmeteo(lat, lon)
correct_openmeteo(data)
