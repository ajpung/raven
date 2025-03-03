from typing import Any, Dict, Tuple
import json
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
Cloud cover: %

__Energy__


__Health__
UV index: 


__Moon__


__Particulate__


__Precip__
Precip. Prob.: %
Precip: mm
Rain: mm
Showers: mm
Evapotranspiration: mm
Vapor pressure deficit: kPa 

__Pressure__
Sea Level: hPa
Surface: hPa

__Radiation__
cape: J/kg
lifted_index:  
convective_inhibition: 
shortwave_radiation_instant: W/m2
direct_radiation_instant: W/m2
diffuse_radiation_instant: W/m2
direct_normal_irradiance_instant: W/m2
global_tilted_irradiance_instant: W/m2
terrestrial_radiation_instant: W/m2

__Soil__
Temperature: C
Moisture: m3/m3

__Solar__
Sun duration: 

__Snow__
Snowfall: cm
Snow depth: m

__Swells__


__Temp__
Temperature: C
Apparent temp: C
Rel. humidity: %
Dewpoint: C
Wet bulb temp: C
Freezing level height: m
Boundary layer height: m

__Trees__


__Visibility__
Visibility: m

__Weeds__


__Waves__


__Wind__
Speed: km/hr
Direction: deg
Gusts: km/h


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
            "temperature_2m",  # 0
            "relative_humidity_2m",  # 1
            "dew_point_2m",  # 2
            "apparent_temperature",  # 3
            "precipitation_probability",  # 4
            "precipitation",  # 5
            "rain",  # 6
            "showers",  # 7
            "snowfall",  # 8
            "snow_depth",  # 9
            "weather_code",  # 10
            "pressure_msl",  # 11
            "surface_pressure",  # 12
            "cloud_cover",  # 13
            "cloud_cover_low",  # 14
            "cloud_cover_mid",  # 15
            "cloud_cover_high",  # 16
            "visibility",  # 17
            "evapotranspiration",  # 18
            "et0_fao_evapotranspiration",  # 19
            "vapour_pressure_deficit",  # 20
            "wind_speed_10m",  # 21
            "wind_speed_80m",  # 22
            "wind_speed_120m",  # 23
            "wind_speed_180m",  # 24
            "wind_direction_10m",  # 25
            "wind_direction_80m",  # 26
            "wind_direction_120m",  # 27
            "wind_direction_180m",  # 28
            "wind_gusts_10m",  # 29
            "temperature_80m",  # 30
            "temperature_120m",  # 31
            "temperature_180m",  # 32
            "soil_temperature_0cm",  # 33
            "soil_temperature_6cm",  # 34
            "soil_temperature_18cm",  # 35
            "soil_temperature_54cm",  # 36
            "soil_moisture_0_to_1cm",  # 37
            "soil_moisture_1_to_3cm",  # 38
            "soil_moisture_3_to_9cm",  # 39
            "soil_moisture_9_to_27cm",  # 40
            "soil_moisture_27_to_81cm",  # 41
            "uv_index",  # 42
            "uv_index_clear_sky",  # 43
            "is_day",  # 44
            "sunshine_duration",  # 45
            "wet_bulb_temperature_2m",  # 46
            "total_column_integrated_water_vapour",  # 47
            "cape",  # 48
            "lifted_index",  # 49
            "convective_inhibition",  # 50
            "freezing_level_height",  # 51
            "boundary_layer_height",  # 52
            "shortwave_radiation",  # 53
            "direct_radiation",  # 54
            "diffuse_radiation",  # 55
            "direct_normal_irradiance",  # 56
            "global_tilted_irradiance",  # 57
            "terrestrial_radiation",  # 58
            "shortwave_radiation_instant",  # 59
            "direct_radiation_instant",  # 60
            "diffuse_radiation_instant",  # 61
            "direct_normal_irradiance_instant",  # 62
            "global_tilted_irradiance_instant",  # 63
            "terrestrial_radiation_instant",  # 64
            "temperature_1000hPa",  # 65
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
            "temperature_30hPa",  # 83
            "relative_humidity_1000hPa",  # 84
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
            "relative_humidity_30hPa",  # 102
            "cloud_cover_1000hPa",  # 103
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
            "cloud_cover_30hPa",  # 121
            "wind_speed_1000hPa",  # 122
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
            "wind_speed_30hPa",  # 140
            "wind_direction_1000hPa",  # 141
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
            "wind_direction_30hPa",  # 159
            "geopotential_height_1000hPa",  # 160
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
            "geopotential_height_30hPa",  # 178
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
    # Read current data
    current = data.Current()
    # Get time of current data (epoch)
    utc_epoch = current.Time()
    # Convert to datetime
    cur_dt = datetime.datetime.fromtimestamp(utc_epoch)
    # Create date string
    ddate = cur_dt.date().strftime("%Y-%m-%d")
    # Create time string
    dtime = cur_dt.time().strftime("%H:%M:%S")
    return data, ddate, dtime, utc_epoch


def fill_openmeteo(
    data, date, time, utc_epoch, json_file: str = "../docs/_static/json_template.json"
):
    current = data.Current()
    # Extract LLA
    lat, lon, alt = data.Latitude(), data.Longitude(), data.Elevation()
    # Vertical altitudes
    altitudes_km = [
        0.1,
        0.32,
        0.5,
        0.8,
        1,
        1.5,
        1.9,
        3,
        4.2,
        5.6,
        7.2,
        9.2,
        10.4,
        11.8,
        13.5,
        15.8,
        17.7,
        19.3,
        22,
    ]
    wind_altitudes_km = [0.01, 0.08, 0.12, 0.18]
    # Apply Unit Corrections
    # kPa -> hPa
    vapor_pressure = current.Variables(20).Value() * 10

    # ----- Read / fill JSON template -----
    openmet_dict = json.load(open(json_file))
    # Datetime
    openmet_dict["datetime"]["date"] = date
    openmet_dict["datetime"]["time"] = time
    openmet_dict["datetime"]["epoch"] = utc_epoch
    # Location
    openmet_dict["location"]["latitutde"] = lat
    openmet_dict["location"]["longitutde"] = lon
    openmet_dict["location"]["altitude"] = alt
    # Clouds
    openmet_dict["data"]["clouds"]["cover"] = current.Variables(13).Value()
    openmet_dict["data"]["clouds"]["tabulated"]["heights"] = altitudes_km
    openmet_dict["data"]["clouds"]["tabulated"]["values"] = [
        current.Variables(i).Value() for i in range(103, 122)
    ]

    # Energy
    openmet_dict["data"]["energy"]["conv_avail_pot"] = current.Variables(48).Value()
    openmet_dict["data"]["energy"]["conv_inhibition"] = current.Variables(50).Value()
    openmet_dict["data"]["energy"]["lifted_index"] = current.Variables(49).Value()
    openmet_dict["data"]["energy"]["bndry_layer_height"] = current.Variables(52).Value()
    # Health
    openmet_dict["data"]["health"]["uv_index"] = current.Variables(42).Value()
    # Precipitation
    openmet_dict["data"]["precipitation"]["probability"] = current.Variables(4).Value()
    openmet_dict["data"]["precipitation"]["rain"]["accumulated"] = current.Variables(
        6
    ).Value()
    openmet_dict["data"]["precipitation"]["snow"]["intensity"] = current.Variables(
        8
    ).Value()
    openmet_dict["data"]["precipitation"]["snow"]["accumulated"] = current.Variables(
        9
    ).Value()
    openmet_dict["data"]["precipitation"]["evapotranspiration"] = current.Variables(
        18
    ).Value()
    # Pressure
    openmet_dict["data"]["pressure"]["sea_level"] = current.Variables(11).Value()
    openmet_dict["data"]["pressure"]["surface"] = current.Variables(12).Value()
    openmet_dict["data"]["pressure"]["vapor_pressure_deficit"] = current.Variables(
        20
    ).Value()
    openmet_dict["data"]["pressure"]["geopotential"]["heights"] = altitudes_km
    openmet_dict["data"]["pressure"]["geopotential"]["values"] = [
        current.Variables(i).Value() for i in range(160, 179)
    ]
    # Radiation
    openmet_dict["data"]["radiation"]["cape"] = current.Variables(48).Value()
    openmet_dict["data"]["radiation"]["lifted_index"] = current.Variables(49).Value()
    openmet_dict["data"]["radiation"]["convective_inhibition"] = current.Variables(
        50
    ).Value()
    openmet_dict["data"]["radiation"]["shortwave"] = current.Variables(59).Value()
    openmet_dict["data"]["radiation"]["direct"] = current.Variables(60).Value()
    openmet_dict["data"]["radiation"]["diffuse"] = current.Variables(61).Value()
    openmet_dict["data"]["radiation"]["global_tilted"] = current.Variables(63).Value()
    openmet_dict["data"]["radiation"]["terrestrial"] = current.Variables(64).Value()
    # Soil
    openmet_dict["data"]["soil"]["temperature"]["depth"] = [0, 6, 18, 54]
    openmet_dict["data"]["soil"]["temperature"]["values"] = [
        current.Variables(i).Value() for i in range(33, 36)
    ]
    openmet_dict["data"]["soil"]["moisture"]["depth"] = [0, 1, 3, 9, 27, 81]
    openmet_dict["data"]["soil"]["moisture"]["values"] = [
        current.Variables(i).Value() for i in range(37, 41)
    ]
    # Sun
    openmet_dict["data"]["sun"]["duration"] = current.Variables(45).Value()
    # Temperature
    openmet_dict["data"]["temperature"]["tabulated"]["heights"] = altitudes_km
    openmet_dict["data"]["temperature"]["tabulated"]["values"] = [
        current.Variables(i).Value() for i in range(65, 84)
    ]
    openmet_dict["data"]["temperature"]["measured"] = current.Variables(0).Value()
    openmet_dict["data"]["temperature"]["apparent"] = current.Variables(3).Value()
    openmet_dict["data"]["temperature"]["dewpoint"] = current.Variables(2).Value()
    openmet_dict["data"]["temperature"]["humidity"] = current.Variables(1).Value()
    # Visibility
    openmet_dict["data"]["visibility"] = current.Variables(17).Value()
    # Wind
    # --- Speed
    openmet_dict["data"]["wind"]["speed"]["heights"] = wind_altitudes_km + altitudes_km
    openmet_dict["data"]["wind"]["speed"]["values"] = [
        current.Variables(i).Value() for i in range(21, 30)
    ] + [current.Variables(i).Value() for i in range(122, 141)]
    # --- Gusts
    openmet_dict["data"]["wind"]["gust"]["heights"] = [10]
    openmet_dict["data"]["wind"]["gust"]["values"] = [current.Variables(29).Value()]
    # --- Direction
    openmet_dict["data"]["wind"]["speed"]["heights"] = wind_altitudes_km + altitudes_km
    openmet_dict["data"]["wind"]["speed"]["values"] = [
        current.Variables(i).Value() for i in range(25, 29)
    ] + [current.Variables(i).Value() for i in range(141, 160)]
    # Return dict
    return openmet_dict


def collect_openmeteo(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects, corrects, and formats weather data from Open-Meteo
    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return tmrw_dict: Weather data from Open-Meteo API
    """
    # Collect data from API
    data = gather_openmeteo(lat, lon)
    # Correct data
    data, date, time, utc_epoch = correct_openmeteo(data)
    # Fill JSON template
    openmeteo_dict = fill_openmeteo(data, date, time, utc_epoch)
    return openmeteo_dict
