from typing import Any, Dict, Tuple

import openmeteo_requests  # type: ignore
import pandas as pd
import requests_cache
from retry_requests import retry  # type: ignore
from pandas import DataFrame

"""
Units taken from https://open-meteo.com/en/docs

__Clouds__
Altitude:
Cover: %

__Energy__
Conv. avail. pot. energ: J/kg

__Health__
Concern: 
Pollute: 
FireIdx: 
GrassIdx:  
mepConcern: 
mepIndex: 

__Moon__
Phase: 

__Particulate__
Matter10: 
Matter25: 
pollutant: 

__Precip__
Hail predict: 
Humidity:
Rain:
Showers:
Ice accum: 
Intensity: 
Probability:
Type: 
Evapotranspiration: mm
Total precip:

__Pressure__
Sea Level:  
Surface Level:  

__Radiation__
Shortwave: 
Direct: 
Diffuse: 
Global tilted irradiance: 

__Soil__
Moisture (Volumetric): m^3/m^3 
Temperature: 

__Solar__
DIF: 
DIR: 
GHI: 

__Snow__
Accumulation: 
Depth:

__Swells__
(Primary & Secondary)
Direction: 
Mean Period: 
Significant Height: 

__Temp__
Dewpoint: 
Temp:
Apparent:  

__Trees__
treeAcacia: 
treeAsh: 
treeBeech: 
treeBirch: 
treeCedar: 
treeCottonwood: 
treeCypress: 
treeElder: 
treeElm: 
treeHemlock: 
treeHickory: 
treeIndex: 
treeJuniper: 
treeMahogany: 
treeMaple: 
treeMulberry: 
treeOak: 
treePine: 
treeSpruce: 
treeSycamore: 
treeWalnut: 
treeWillow: 

__Visibility__
visibility:  

__Weeds__
weedGrassIndex: 
WeedIndex: 

__Waves__
SignificantHeight: 
Direction: 
MeanPeriod: 

__Wind__
Speed: 
Gust: 
Direction:  
windWaveSignificantHeight: 
windWaveDirection: 
windWaveMeanPeriod: 
"""


def gather_openmeteo(lat: float, lon: float):
    # NOTE:
    #   - Current conditions are based on 15-minutely weather model data
    #   - Every weather variable available in hourly data is available as current condition as well!

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "rain",
            "showers",
            "snowfall",
            "weather_code",
            "cloud_cover",
            "pressure_msl",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
        ],
        "minutely_15": [
            "temperature_2m",
            "relative_humidity_2m",
            "dew_point_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "snowfall",
            "snowfall_height",
            "freezing_level_height",
            "sunshine_duration",
            "weather_code",
            "wind_speed_10m",
            "wind_speed_80m",
            "wind_direction_10m",
            "wind_direction_80m",
            "wind_gusts_10m",
            "visibility",
            "cape",
            "lightning_potential",
            "is_day",
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
        ],
        "hourly": [
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
        "past_hours": 1,
        "models": [
            "best_match",
            "ecmwf_ifs04",
            "ecmwf_ifs025",
            "ecmwf_aifs025",
            "ecmwf_aifs025_single",
            "cma_grapes_global",
            "bom_access_global",
            "gfs_seamless",
            "gfs_global",
            "gfs_hrrr",
            "ncep_nbm_conus",
            "gfs_graphcast025",
            "jma_seamless",
            "jma_msm",
            "jma_gsm",
            "icon_seamless",
            "icon_global",
            "icon_eu",
            "icon_d2",
            "gem_seamless",
            "gem_global",
            "gem_regional",
            "gem_hrdps_continental",
            "meteofrance_seamless",
            "meteofrance_arpege_world",
            "meteofrance_arpege_europe",
            "meteofrance_arome_france",
            "meteofrance_arome_france_hd",
            "arpae_cosmo_seamless",
            "arpae_cosmo_2i",
            "arpae_cosmo_5m",
            "metno_seamless",
            "metno_nordic",
            "knmi_seamless",
            "knmi_harmonie_arome_europe",
            "knmi_harmonie_arome_netherlands",
            "dmi_seamless",
            "dmi_harmonie_arome_europe",
            "ukmo_seamless",
            "ukmo_global_deterministic_10km",
            "ukmo_uk_deterministic_2km",
        ],
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()

    current_temperature_2m = current.Variables(0).Value()

    current_relative_humidity_2m = current.Variables(1).Value()

    current_apparent_temperature = current.Variables(2).Value()

    current_is_day = current.Variables(3).Value()

    current_precipitation = current.Variables(4).Value()

    current_rain = current.Variables(5).Value()

    current_showers = current.Variables(6).Value()

    current_snowfall = current.Variables(7).Value()

    current_weather_code = current.Variables(8).Value()

    current_cloud_cover = current.Variables(9).Value()

    current_pressure_msl = current.Variables(10).Value()

    current_surface_pressure = current.Variables(11).Value()

    current_wind_speed_10m = current.Variables(12).Value()

    current_wind_direction_10m = current.Variables(13).Value()

    current_wind_gusts_10m = current.Variables(14).Value()

    print(f"Current time {current.Time()}")

    print(f"Current temperature_2m {current_temperature_2m}")
    print(f"Current relative_humidity_2m {current_relative_humidity_2m}")
    print(f"Current apparent_temperature {current_apparent_temperature}")
    print(f"Current is_day {current_is_day}")
    print(f"Current precipitation {current_precipitation}")
    print(f"Current rain {current_rain}")
    print(f"Current showers {current_showers}")
    print(f"Current snowfall {current_snowfall}")
    print(f"Current weather_code {current_weather_code}")
    print(f"Current cloud_cover {current_cloud_cover}")
    print(f"Current pressure_msl {current_pressure_msl}")
    print(f"Current surface_pressure {current_surface_pressure}")
    print(f"Current wind_speed_10m {current_wind_speed_10m}")
    print(f"Current wind_direction_10m {current_wind_direction_10m}")
    print(f"Current wind_gusts_10m {current_wind_gusts_10m}")
    # Process minutely_15 data. The order of variables needs to be the same as requested.
    minutely_15 = response.Minutely15()
    minutely_15_temperature_2m = minutely_15.Variables(0).ValuesAsNumpy()
    minutely_15_relative_humidity_2m = minutely_15.Variables(1).ValuesAsNumpy()
    minutely_15_dew_point_2m = minutely_15.Variables(2).ValuesAsNumpy()
    minutely_15_apparent_temperature = minutely_15.Variables(3).ValuesAsNumpy()
    minutely_15_precipitation = minutely_15.Variables(4).ValuesAsNumpy()
    minutely_15_rain = minutely_15.Variables(5).ValuesAsNumpy()
    minutely_15_snowfall = minutely_15.Variables(6).ValuesAsNumpy()
    minutely_15_snowfall_height = minutely_15.Variables(7).ValuesAsNumpy()
    minutely_15_freezing_level_height = minutely_15.Variables(8).ValuesAsNumpy()
    minutely_15_sunshine_duration = minutely_15.Variables(9).ValuesAsNumpy()
    minutely_15_weather_code = minutely_15.Variables(10).ValuesAsNumpy()
    minutely_15_wind_speed_10m = minutely_15.Variables(11).ValuesAsNumpy()
    minutely_15_wind_speed_80m = minutely_15.Variables(12).ValuesAsNumpy()
    minutely_15_wind_direction_10m = minutely_15.Variables(13).ValuesAsNumpy()
    minutely_15_wind_direction_80m = minutely_15.Variables(14).ValuesAsNumpy()
    minutely_15_wind_gusts_10m = minutely_15.Variables(15).ValuesAsNumpy()
    minutely_15_visibility = minutely_15.Variables(16).ValuesAsNumpy()
    minutely_15_cape = minutely_15.Variables(17).ValuesAsNumpy()
    minutely_15_lightning_potential = minutely_15.Variables(18).ValuesAsNumpy()
    minutely_15_is_day = minutely_15.Variables(19).ValuesAsNumpy()
    minutely_15_shortwave_radiation = minutely_15.Variables(20).ValuesAsNumpy()
    minutely_15_direct_radiation = minutely_15.Variables(21).ValuesAsNumpy()
    minutely_15_diffuse_radiation = minutely_15.Variables(22).ValuesAsNumpy()
    minutely_15_direct_normal_irradiance = minutely_15.Variables(23).ValuesAsNumpy()
    minutely_15_global_tilted_irradiance = minutely_15.Variables(24).ValuesAsNumpy()
    minutely_15_terrestrial_radiation = minutely_15.Variables(25).ValuesAsNumpy()
    minutely_15_shortwave_radiation_instant = minutely_15.Variables(26).ValuesAsNumpy()
    minutely_15_direct_radiation_instant = minutely_15.Variables(27).ValuesAsNumpy()
    minutely_15_diffuse_radiation_instant = minutely_15.Variables(28).ValuesAsNumpy()
    minutely_15_direct_normal_irradiance_instant = minutely_15.Variables(
        29
    ).ValuesAsNumpy()
    minutely_15_global_tilted_irradiance_instant = minutely_15.Variables(
        30
    ).ValuesAsNumpy()
    minutely_15_terrestrial_radiation_instant = minutely_15.Variables(
        31
    ).ValuesAsNumpy()

    minutely_15_data = {
        "date": pd.date_range(
            start=pd.to_datetime(minutely_15.Time(), unit="s", utc=True),
            end=pd.to_datetime(minutely_15.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=minutely_15.Interval()),
            inclusive="left",
        )
    }

    minutely_15_data["temperature_2m"] = minutely_15_temperature_2m
    minutely_15_data["relative_humidity_2m"] = minutely_15_relative_humidity_2m
    minutely_15_data["dew_point_2m"] = minutely_15_dew_point_2m
    minutely_15_data["apparent_temperature"] = minutely_15_apparent_temperature
    minutely_15_data["precipitation"] = minutely_15_precipitation
    minutely_15_data["rain"] = minutely_15_rain
    minutely_15_data["snowfall"] = minutely_15_snowfall
    minutely_15_data["snowfall_height"] = minutely_15_snowfall_height
    minutely_15_data["freezing_level_height"] = minutely_15_freezing_level_height
    minutely_15_data["sunshine_duration"] = minutely_15_sunshine_duration
    minutely_15_data["weather_code"] = minutely_15_weather_code
    minutely_15_data["wind_speed_10m"] = minutely_15_wind_speed_10m
    minutely_15_data["wind_speed_80m"] = minutely_15_wind_speed_80m
    minutely_15_data["wind_direction_10m"] = minutely_15_wind_direction_10m
    minutely_15_data["wind_direction_80m"] = minutely_15_wind_direction_80m
    minutely_15_data["wind_gusts_10m"] = minutely_15_wind_gusts_10m
    minutely_15_data["visibility"] = minutely_15_visibility
    minutely_15_data["cape"] = minutely_15_cape
    minutely_15_data["lightning_potential"] = minutely_15_lightning_potential
    minutely_15_data["is_day"] = minutely_15_is_day
    minutely_15_data["shortwave_radiation"] = minutely_15_shortwave_radiation
    minutely_15_data["direct_radiation"] = minutely_15_direct_radiation
    minutely_15_data["diffuse_radiation"] = minutely_15_diffuse_radiation
    minutely_15_data["direct_normal_irradiance"] = minutely_15_direct_normal_irradiance
    minutely_15_data["global_tilted_irradiance"] = minutely_15_global_tilted_irradiance
    minutely_15_data["terrestrial_radiation"] = minutely_15_terrestrial_radiation
    minutely_15_data["shortwave_radiation_instant"] = (
        minutely_15_shortwave_radiation_instant
    )
    minutely_15_data["direct_radiation_instant"] = minutely_15_direct_radiation_instant
    minutely_15_data["diffuse_radiation_instant"] = (
        minutely_15_diffuse_radiation_instant
    )
    minutely_15_data["direct_normal_irradiance_instant"] = (
        minutely_15_direct_normal_irradiance_instant
    )
    minutely_15_data["global_tilted_irradiance_instant"] = (
        minutely_15_global_tilted_irradiance_instant
    )
    minutely_15_data["terrestrial_radiation_instant"] = (
        minutely_15_terrestrial_radiation_instant
    )

    minutely_15_dataframe = pd.DataFrame(data=minutely_15_data)
    print(minutely_15_dataframe)

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(4).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(5).ValuesAsNumpy()
    hourly_rain = hourly.Variables(6).ValuesAsNumpy()
    hourly_showers = hourly.Variables(7).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(8).ValuesAsNumpy()
    hourly_snow_depth = hourly.Variables(9).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(10).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(11).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(12).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(13).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(14).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(15).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(16).ValuesAsNumpy()
    hourly_visibility = hourly.Variables(17).ValuesAsNumpy()
    hourly_evapotranspiration = hourly.Variables(18).ValuesAsNumpy()
    hourly_et0_fao_evapotranspiration = hourly.Variables(19).ValuesAsNumpy()
    hourly_vapour_pressure_deficit = hourly.Variables(20).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(21).ValuesAsNumpy()
    hourly_wind_speed_80m = hourly.Variables(22).ValuesAsNumpy()
    hourly_wind_speed_120m = hourly.Variables(23).ValuesAsNumpy()
    hourly_wind_speed_180m = hourly.Variables(24).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(25).ValuesAsNumpy()
    hourly_wind_direction_80m = hourly.Variables(26).ValuesAsNumpy()
    hourly_wind_direction_120m = hourly.Variables(27).ValuesAsNumpy()
    hourly_wind_direction_180m = hourly.Variables(28).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(29).ValuesAsNumpy()
    hourly_temperature_80m = hourly.Variables(30).ValuesAsNumpy()
    hourly_temperature_120m = hourly.Variables(31).ValuesAsNumpy()
    hourly_temperature_180m = hourly.Variables(32).ValuesAsNumpy()
    hourly_soil_temperature_0cm = hourly.Variables(33).ValuesAsNumpy()
    hourly_soil_temperature_6cm = hourly.Variables(34).ValuesAsNumpy()
    hourly_soil_temperature_18cm = hourly.Variables(35).ValuesAsNumpy()
    hourly_soil_temperature_54cm = hourly.Variables(36).ValuesAsNumpy()
    hourly_soil_moisture_0_to_1cm = hourly.Variables(37).ValuesAsNumpy()
    hourly_soil_moisture_1_to_3cm = hourly.Variables(38).ValuesAsNumpy()
    hourly_soil_moisture_3_to_9cm = hourly.Variables(39).ValuesAsNumpy()
    hourly_soil_moisture_9_to_27cm = hourly.Variables(40).ValuesAsNumpy()
    hourly_soil_moisture_27_to_81cm = hourly.Variables(41).ValuesAsNumpy()
    hourly_uv_index = hourly.Variables(42).ValuesAsNumpy()
    hourly_uv_index_clear_sky = hourly.Variables(43).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(44).ValuesAsNumpy()
    hourly_sunshine_duration = hourly.Variables(45).ValuesAsNumpy()
    hourly_wet_bulb_temperature_2m = hourly.Variables(46).ValuesAsNumpy()
    hourly_total_column_integrated_water_vapour = hourly.Variables(47).ValuesAsNumpy()
    hourly_cape = hourly.Variables(48).ValuesAsNumpy()
    hourly_lifted_index = hourly.Variables(49).ValuesAsNumpy()
    hourly_convective_inhibition = hourly.Variables(50).ValuesAsNumpy()
    hourly_freezing_level_height = hourly.Variables(51).ValuesAsNumpy()
    hourly_boundary_layer_height = hourly.Variables(52).ValuesAsNumpy()
    hourly_shortwave_radiation = hourly.Variables(53).ValuesAsNumpy()
    hourly_direct_radiation = hourly.Variables(54).ValuesAsNumpy()
    hourly_diffuse_radiation = hourly.Variables(55).ValuesAsNumpy()
    hourly_direct_normal_irradiance = hourly.Variables(56).ValuesAsNumpy()
    hourly_global_tilted_irradiance = hourly.Variables(57).ValuesAsNumpy()
    hourly_terrestrial_radiation = hourly.Variables(58).ValuesAsNumpy()
    hourly_shortwave_radiation_instant = hourly.Variables(59).ValuesAsNumpy()
    hourly_direct_radiation_instant = hourly.Variables(60).ValuesAsNumpy()
    hourly_diffuse_radiation_instant = hourly.Variables(61).ValuesAsNumpy()
    hourly_direct_normal_irradiance_instant = hourly.Variables(62).ValuesAsNumpy()
    hourly_global_tilted_irradiance_instant = hourly.Variables(63).ValuesAsNumpy()
    hourly_terrestrial_radiation_instant = hourly.Variables(64).ValuesAsNumpy()
    hourly_temperature_1000hPa = hourly.Variables(65).ValuesAsNumpy()
    hourly_temperature_975hPa = hourly.Variables(66).ValuesAsNumpy()
    hourly_temperature_950hPa = hourly.Variables(67).ValuesAsNumpy()
    hourly_temperature_925hPa = hourly.Variables(68).ValuesAsNumpy()
    hourly_temperature_900hPa = hourly.Variables(69).ValuesAsNumpy()
    hourly_temperature_850hPa = hourly.Variables(70).ValuesAsNumpy()
    hourly_temperature_800hPa = hourly.Variables(71).ValuesAsNumpy()
    hourly_temperature_700hPa = hourly.Variables(72).ValuesAsNumpy()
    hourly_temperature_600hPa = hourly.Variables(73).ValuesAsNumpy()
    hourly_temperature_500hPa = hourly.Variables(74).ValuesAsNumpy()
    hourly_temperature_400hPa = hourly.Variables(75).ValuesAsNumpy()
    hourly_temperature_300hPa = hourly.Variables(76).ValuesAsNumpy()
    hourly_temperature_250hPa = hourly.Variables(77).ValuesAsNumpy()
    hourly_temperature_200hPa = hourly.Variables(78).ValuesAsNumpy()
    hourly_temperature_150hPa = hourly.Variables(79).ValuesAsNumpy()
    hourly_temperature_100hPa = hourly.Variables(80).ValuesAsNumpy()
    hourly_temperature_70hPa = hourly.Variables(81).ValuesAsNumpy()
    hourly_temperature_50hPa = hourly.Variables(82).ValuesAsNumpy()
    hourly_temperature_30hPa = hourly.Variables(83).ValuesAsNumpy()
    hourly_relative_humidity_1000hPa = hourly.Variables(84).ValuesAsNumpy()
    hourly_relative_humidity_975hPa = hourly.Variables(85).ValuesAsNumpy()
    hourly_relative_humidity_950hPa = hourly.Variables(86).ValuesAsNumpy()
    hourly_relative_humidity_925hPa = hourly.Variables(87).ValuesAsNumpy()
    hourly_relative_humidity_900hPa = hourly.Variables(88).ValuesAsNumpy()
    hourly_relative_humidity_850hPa = hourly.Variables(89).ValuesAsNumpy()
    hourly_relative_humidity_800hPa = hourly.Variables(90).ValuesAsNumpy()
    hourly_relative_humidity_700hPa = hourly.Variables(91).ValuesAsNumpy()
    hourly_relative_humidity_600hPa = hourly.Variables(92).ValuesAsNumpy()
    hourly_relative_humidity_500hPa = hourly.Variables(93).ValuesAsNumpy()
    hourly_relative_humidity_400hPa = hourly.Variables(94).ValuesAsNumpy()
    hourly_relative_humidity_300hPa = hourly.Variables(95).ValuesAsNumpy()
    hourly_relative_humidity_250hPa = hourly.Variables(96).ValuesAsNumpy()
    hourly_relative_humidity_200hPa = hourly.Variables(97).ValuesAsNumpy()
    hourly_relative_humidity_150hPa = hourly.Variables(98).ValuesAsNumpy()
    hourly_relative_humidity_100hPa = hourly.Variables(99).ValuesAsNumpy()
    hourly_relative_humidity_70hPa = hourly.Variables(100).ValuesAsNumpy()
    hourly_relative_humidity_50hPa = hourly.Variables(101).ValuesAsNumpy()
    hourly_relative_humidity_30hPa = hourly.Variables(102).ValuesAsNumpy()
    hourly_cloud_cover_1000hPa = hourly.Variables(103).ValuesAsNumpy()
    hourly_cloud_cover_975hPa = hourly.Variables(104).ValuesAsNumpy()
    hourly_cloud_cover_950hPa = hourly.Variables(105).ValuesAsNumpy()
    hourly_cloud_cover_925hPa = hourly.Variables(106).ValuesAsNumpy()
    hourly_cloud_cover_900hPa = hourly.Variables(107).ValuesAsNumpy()
    hourly_cloud_cover_850hPa = hourly.Variables(108).ValuesAsNumpy()
    hourly_cloud_cover_800hPa = hourly.Variables(109).ValuesAsNumpy()
    hourly_cloud_cover_700hPa = hourly.Variables(110).ValuesAsNumpy()
    hourly_cloud_cover_600hPa = hourly.Variables(111).ValuesAsNumpy()
    hourly_cloud_cover_500hPa = hourly.Variables(112).ValuesAsNumpy()
    hourly_cloud_cover_400hPa = hourly.Variables(113).ValuesAsNumpy()
    hourly_cloud_cover_300hPa = hourly.Variables(114).ValuesAsNumpy()
    hourly_cloud_cover_250hPa = hourly.Variables(115).ValuesAsNumpy()
    hourly_cloud_cover_200hPa = hourly.Variables(116).ValuesAsNumpy()
    hourly_cloud_cover_150hPa = hourly.Variables(117).ValuesAsNumpy()
    hourly_cloud_cover_100hPa = hourly.Variables(118).ValuesAsNumpy()
    hourly_cloud_cover_70hPa = hourly.Variables(119).ValuesAsNumpy()
    hourly_cloud_cover_50hPa = hourly.Variables(120).ValuesAsNumpy()
    hourly_cloud_cover_30hPa = hourly.Variables(121).ValuesAsNumpy()
    hourly_wind_speed_1000hPa = hourly.Variables(122).ValuesAsNumpy()
    hourly_wind_speed_975hPa = hourly.Variables(123).ValuesAsNumpy()
    hourly_wind_speed_950hPa = hourly.Variables(124).ValuesAsNumpy()
    hourly_wind_speed_925hPa = hourly.Variables(125).ValuesAsNumpy()
    hourly_wind_speed_900hPa = hourly.Variables(126).ValuesAsNumpy()
    hourly_wind_speed_850hPa = hourly.Variables(127).ValuesAsNumpy()
    hourly_wind_speed_800hPa = hourly.Variables(128).ValuesAsNumpy()
    hourly_wind_speed_700hPa = hourly.Variables(129).ValuesAsNumpy()
    hourly_wind_speed_600hPa = hourly.Variables(130).ValuesAsNumpy()
    hourly_wind_speed_500hPa = hourly.Variables(131).ValuesAsNumpy()
    hourly_wind_speed_400hPa = hourly.Variables(132).ValuesAsNumpy()
    hourly_wind_speed_300hPa = hourly.Variables(133).ValuesAsNumpy()
    hourly_wind_speed_250hPa = hourly.Variables(134).ValuesAsNumpy()
    hourly_wind_speed_200hPa = hourly.Variables(135).ValuesAsNumpy()
    hourly_wind_speed_150hPa = hourly.Variables(136).ValuesAsNumpy()
    hourly_wind_speed_100hPa = hourly.Variables(137).ValuesAsNumpy()
    hourly_wind_speed_70hPa = hourly.Variables(138).ValuesAsNumpy()
    hourly_wind_speed_50hPa = hourly.Variables(139).ValuesAsNumpy()
    hourly_wind_speed_30hPa = hourly.Variables(140).ValuesAsNumpy()
    hourly_wind_direction_1000hPa = hourly.Variables(141).ValuesAsNumpy()
    hourly_wind_direction_975hPa = hourly.Variables(142).ValuesAsNumpy()
    hourly_wind_direction_950hPa = hourly.Variables(143).ValuesAsNumpy()
    hourly_wind_direction_925hPa = hourly.Variables(144).ValuesAsNumpy()
    hourly_wind_direction_900hPa = hourly.Variables(145).ValuesAsNumpy()
    hourly_wind_direction_850hPa = hourly.Variables(146).ValuesAsNumpy()
    hourly_wind_direction_800hPa = hourly.Variables(147).ValuesAsNumpy()
    hourly_wind_direction_700hPa = hourly.Variables(148).ValuesAsNumpy()
    hourly_wind_direction_600hPa = hourly.Variables(149).ValuesAsNumpy()
    hourly_wind_direction_500hPa = hourly.Variables(150).ValuesAsNumpy()
    hourly_wind_direction_400hPa = hourly.Variables(151).ValuesAsNumpy()
    hourly_wind_direction_300hPa = hourly.Variables(152).ValuesAsNumpy()
    hourly_wind_direction_250hPa = hourly.Variables(153).ValuesAsNumpy()
    hourly_wind_direction_200hPa = hourly.Variables(154).ValuesAsNumpy()
    hourly_wind_direction_150hPa = hourly.Variables(155).ValuesAsNumpy()
    hourly_wind_direction_100hPa = hourly.Variables(156).ValuesAsNumpy()
    hourly_wind_direction_70hPa = hourly.Variables(157).ValuesAsNumpy()
    hourly_wind_direction_50hPa = hourly.Variables(158).ValuesAsNumpy()
    hourly_wind_direction_30hPa = hourly.Variables(159).ValuesAsNumpy()
    hourly_geopotential_height_1000hPa = hourly.Variables(160).ValuesAsNumpy()
    hourly_geopotential_height_975hPa = hourly.Variables(161).ValuesAsNumpy()
    hourly_geopotential_height_950hPa = hourly.Variables(162).ValuesAsNumpy()
    hourly_geopotential_height_925hPa = hourly.Variables(163).ValuesAsNumpy()
    hourly_geopotential_height_900hPa = hourly.Variables(164).ValuesAsNumpy()
    hourly_geopotential_height_850hPa = hourly.Variables(165).ValuesAsNumpy()
    hourly_geopotential_height_800hPa = hourly.Variables(166).ValuesAsNumpy()
    hourly_geopotential_height_700hPa = hourly.Variables(167).ValuesAsNumpy()
    hourly_geopotential_height_600hPa = hourly.Variables(168).ValuesAsNumpy()
    hourly_geopotential_height_500hPa = hourly.Variables(169).ValuesAsNumpy()
    hourly_geopotential_height_400hPa = hourly.Variables(170).ValuesAsNumpy()
    hourly_geopotential_height_300hPa = hourly.Variables(171).ValuesAsNumpy()
    hourly_geopotential_height_250hPa = hourly.Variables(172).ValuesAsNumpy()
    hourly_geopotential_height_200hPa = hourly.Variables(173).ValuesAsNumpy()
    hourly_geopotential_height_150hPa = hourly.Variables(174).ValuesAsNumpy()
    hourly_geopotential_height_100hPa = hourly.Variables(175).ValuesAsNumpy()
    hourly_geopotential_height_70hPa = hourly.Variables(176).ValuesAsNumpy()
    hourly_geopotential_height_50hPa = hourly.Variables(177).ValuesAsNumpy()
    hourly_geopotential_height_30hPa = hourly.Variables(178).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["rain"] = hourly_rain
    hourly_data["showers"] = hourly_showers
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["snow_depth"] = hourly_snow_depth
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["pressure_msl"] = hourly_pressure_msl
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
    hourly_data["visibility"] = hourly_visibility
    hourly_data["evapotranspiration"] = hourly_evapotranspiration
    hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
    hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
    hourly_data["wind_speed_120m"] = hourly_wind_speed_120m
    hourly_data["wind_speed_180m"] = hourly_wind_speed_180m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["wind_direction_80m"] = hourly_wind_direction_80m
    hourly_data["wind_direction_120m"] = hourly_wind_direction_120m
    hourly_data["wind_direction_180m"] = hourly_wind_direction_180m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
    hourly_data["temperature_80m"] = hourly_temperature_80m
    hourly_data["temperature_120m"] = hourly_temperature_120m
    hourly_data["temperature_180m"] = hourly_temperature_180m
    hourly_data["soil_temperature_0cm"] = hourly_soil_temperature_0cm
    hourly_data["soil_temperature_6cm"] = hourly_soil_temperature_6cm
    hourly_data["soil_temperature_18cm"] = hourly_soil_temperature_18cm
    hourly_data["soil_temperature_54cm"] = hourly_soil_temperature_54cm
    hourly_data["soil_moisture_0_to_1cm"] = hourly_soil_moisture_0_to_1cm
    hourly_data["soil_moisture_1_to_3cm"] = hourly_soil_moisture_1_to_3cm
    hourly_data["soil_moisture_3_to_9cm"] = hourly_soil_moisture_3_to_9cm
    hourly_data["soil_moisture_9_to_27cm"] = hourly_soil_moisture_9_to_27cm
    hourly_data["soil_moisture_27_to_81cm"] = hourly_soil_moisture_27_to_81cm
    hourly_data["uv_index"] = hourly_uv_index
    hourly_data["uv_index_clear_sky"] = hourly_uv_index_clear_sky
    hourly_data["is_day"] = hourly_is_day
    hourly_data["sunshine_duration"] = hourly_sunshine_duration
    hourly_data["wet_bulb_temperature_2m"] = hourly_wet_bulb_temperature_2m
    hourly_data["total_column_integrated_water_vapour"] = (
        hourly_total_column_integrated_water_vapour
    )
    hourly_data["cape"] = hourly_cape
    hourly_data["lifted_index"] = hourly_lifted_index
    hourly_data["convective_inhibition"] = hourly_convective_inhibition
    hourly_data["freezing_level_height"] = hourly_freezing_level_height
    hourly_data["boundary_layer_height"] = hourly_boundary_layer_height
    hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
    hourly_data["direct_radiation"] = hourly_direct_radiation
    hourly_data["diffuse_radiation"] = hourly_diffuse_radiation
    hourly_data["direct_normal_irradiance"] = hourly_direct_normal_irradiance
    hourly_data["global_tilted_irradiance"] = hourly_global_tilted_irradiance
    hourly_data["terrestrial_radiation"] = hourly_terrestrial_radiation
    hourly_data["shortwave_radiation_instant"] = hourly_shortwave_radiation_instant
    hourly_data["direct_radiation_instant"] = hourly_direct_radiation_instant
    hourly_data["diffuse_radiation_instant"] = hourly_diffuse_radiation_instant
    hourly_data["direct_normal_irradiance_instant"] = (
        hourly_direct_normal_irradiance_instant
    )
    hourly_data["global_tilted_irradiance_instant"] = (
        hourly_global_tilted_irradiance_instant
    )
    hourly_data["terrestrial_radiation_instant"] = hourly_terrestrial_radiation_instant
    hourly_data["temperature_1000hPa"] = hourly_temperature_1000hPa
    hourly_data["temperature_975hPa"] = hourly_temperature_975hPa
    hourly_data["temperature_950hPa"] = hourly_temperature_950hPa
    hourly_data["temperature_925hPa"] = hourly_temperature_925hPa
    hourly_data["temperature_900hPa"] = hourly_temperature_900hPa
    hourly_data["temperature_850hPa"] = hourly_temperature_850hPa
    hourly_data["temperature_800hPa"] = hourly_temperature_800hPa
    hourly_data["temperature_700hPa"] = hourly_temperature_700hPa
    hourly_data["temperature_600hPa"] = hourly_temperature_600hPa
    hourly_data["temperature_500hPa"] = hourly_temperature_500hPa
    hourly_data["temperature_400hPa"] = hourly_temperature_400hPa
    hourly_data["temperature_300hPa"] = hourly_temperature_300hPa
    hourly_data["temperature_250hPa"] = hourly_temperature_250hPa
    hourly_data["temperature_200hPa"] = hourly_temperature_200hPa
    hourly_data["temperature_150hPa"] = hourly_temperature_150hPa
    hourly_data["temperature_100hPa"] = hourly_temperature_100hPa
    hourly_data["temperature_70hPa"] = hourly_temperature_70hPa
    hourly_data["temperature_50hPa"] = hourly_temperature_50hPa
    hourly_data["temperature_30hPa"] = hourly_temperature_30hPa
    hourly_data["relative_humidity_1000hPa"] = hourly_relative_humidity_1000hPa
    hourly_data["relative_humidity_975hPa"] = hourly_relative_humidity_975hPa
    hourly_data["relative_humidity_950hPa"] = hourly_relative_humidity_950hPa
    hourly_data["relative_humidity_925hPa"] = hourly_relative_humidity_925hPa
    hourly_data["relative_humidity_900hPa"] = hourly_relative_humidity_900hPa
    hourly_data["relative_humidity_850hPa"] = hourly_relative_humidity_850hPa
    hourly_data["relative_humidity_800hPa"] = hourly_relative_humidity_800hPa
    hourly_data["relative_humidity_700hPa"] = hourly_relative_humidity_700hPa
    hourly_data["relative_humidity_600hPa"] = hourly_relative_humidity_600hPa
    hourly_data["relative_humidity_500hPa"] = hourly_relative_humidity_500hPa
    hourly_data["relative_humidity_400hPa"] = hourly_relative_humidity_400hPa
    hourly_data["relative_humidity_300hPa"] = hourly_relative_humidity_300hPa
    hourly_data["relative_humidity_250hPa"] = hourly_relative_humidity_250hPa
    hourly_data["relative_humidity_200hPa"] = hourly_relative_humidity_200hPa
    hourly_data["relative_humidity_150hPa"] = hourly_relative_humidity_150hPa
    hourly_data["relative_humidity_100hPa"] = hourly_relative_humidity_100hPa
    hourly_data["relative_humidity_70hPa"] = hourly_relative_humidity_70hPa
    hourly_data["relative_humidity_50hPa"] = hourly_relative_humidity_50hPa
    hourly_data["relative_humidity_30hPa"] = hourly_relative_humidity_30hPa
    hourly_data["cloud_cover_1000hPa"] = hourly_cloud_cover_1000hPa
    hourly_data["cloud_cover_975hPa"] = hourly_cloud_cover_975hPa
    hourly_data["cloud_cover_950hPa"] = hourly_cloud_cover_950hPa
    hourly_data["cloud_cover_925hPa"] = hourly_cloud_cover_925hPa
    hourly_data["cloud_cover_900hPa"] = hourly_cloud_cover_900hPa
    hourly_data["cloud_cover_850hPa"] = hourly_cloud_cover_850hPa
    hourly_data["cloud_cover_800hPa"] = hourly_cloud_cover_800hPa
    hourly_data["cloud_cover_700hPa"] = hourly_cloud_cover_700hPa
    hourly_data["cloud_cover_600hPa"] = hourly_cloud_cover_600hPa
    hourly_data["cloud_cover_500hPa"] = hourly_cloud_cover_500hPa
    hourly_data["cloud_cover_400hPa"] = hourly_cloud_cover_400hPa
    hourly_data["cloud_cover_300hPa"] = hourly_cloud_cover_300hPa
    hourly_data["cloud_cover_250hPa"] = hourly_cloud_cover_250hPa
    hourly_data["cloud_cover_200hPa"] = hourly_cloud_cover_200hPa
    hourly_data["cloud_cover_150hPa"] = hourly_cloud_cover_150hPa
    hourly_data["cloud_cover_100hPa"] = hourly_cloud_cover_100hPa
    hourly_data["cloud_cover_70hPa"] = hourly_cloud_cover_70hPa
    hourly_data["cloud_cover_50hPa"] = hourly_cloud_cover_50hPa
    hourly_data["cloud_cover_30hPa"] = hourly_cloud_cover_30hPa
    hourly_data["wind_speed_1000hPa"] = hourly_wind_speed_1000hPa
    hourly_data["wind_speed_975hPa"] = hourly_wind_speed_975hPa
    hourly_data["wind_speed_950hPa"] = hourly_wind_speed_950hPa
    hourly_data["wind_speed_925hPa"] = hourly_wind_speed_925hPa
    hourly_data["wind_speed_900hPa"] = hourly_wind_speed_900hPa
    hourly_data["wind_speed_850hPa"] = hourly_wind_speed_850hPa
    hourly_data["wind_speed_800hPa"] = hourly_wind_speed_800hPa
    hourly_data["wind_speed_700hPa"] = hourly_wind_speed_700hPa
    hourly_data["wind_speed_600hPa"] = hourly_wind_speed_600hPa
    hourly_data["wind_speed_500hPa"] = hourly_wind_speed_500hPa
    hourly_data["wind_speed_400hPa"] = hourly_wind_speed_400hPa
    hourly_data["wind_speed_300hPa"] = hourly_wind_speed_300hPa
    hourly_data["wind_speed_250hPa"] = hourly_wind_speed_250hPa
    hourly_data["wind_speed_200hPa"] = hourly_wind_speed_200hPa
    hourly_data["wind_speed_150hPa"] = hourly_wind_speed_150hPa
    hourly_data["wind_speed_100hPa"] = hourly_wind_speed_100hPa
    hourly_data["wind_speed_70hPa"] = hourly_wind_speed_70hPa
    hourly_data["wind_speed_50hPa"] = hourly_wind_speed_50hPa
    hourly_data["wind_speed_30hPa"] = hourly_wind_speed_30hPa
    hourly_data["wind_direction_1000hPa"] = hourly_wind_direction_1000hPa
    hourly_data["wind_direction_975hPa"] = hourly_wind_direction_975hPa
    hourly_data["wind_direction_950hPa"] = hourly_wind_direction_950hPa
    hourly_data["wind_direction_925hPa"] = hourly_wind_direction_925hPa
    hourly_data["wind_direction_900hPa"] = hourly_wind_direction_900hPa
    hourly_data["wind_direction_850hPa"] = hourly_wind_direction_850hPa
    hourly_data["wind_direction_800hPa"] = hourly_wind_direction_800hPa
    hourly_data["wind_direction_700hPa"] = hourly_wind_direction_700hPa
    hourly_data["wind_direction_600hPa"] = hourly_wind_direction_600hPa
    hourly_data["wind_direction_500hPa"] = hourly_wind_direction_500hPa
    hourly_data["wind_direction_400hPa"] = hourly_wind_direction_400hPa
    hourly_data["wind_direction_300hPa"] = hourly_wind_direction_300hPa
    hourly_data["wind_direction_250hPa"] = hourly_wind_direction_250hPa
    hourly_data["wind_direction_200hPa"] = hourly_wind_direction_200hPa
    hourly_data["wind_direction_150hPa"] = hourly_wind_direction_150hPa
    hourly_data["wind_direction_100hPa"] = hourly_wind_direction_100hPa
    hourly_data["wind_direction_70hPa"] = hourly_wind_direction_70hPa
    hourly_data["wind_direction_50hPa"] = hourly_wind_direction_50hPa
    hourly_data["wind_direction_30hPa"] = hourly_wind_direction_30hPa
    hourly_data["geopotential_height_1000hPa"] = hourly_geopotential_height_1000hPa
    hourly_data["geopotential_height_975hPa"] = hourly_geopotential_height_975hPa
    hourly_data["geopotential_height_950hPa"] = hourly_geopotential_height_950hPa
    hourly_data["geopotential_height_925hPa"] = hourly_geopotential_height_925hPa
    hourly_data["geopotential_height_900hPa"] = hourly_geopotential_height_900hPa
    hourly_data["geopotential_height_850hPa"] = hourly_geopotential_height_850hPa
    hourly_data["geopotential_height_800hPa"] = hourly_geopotential_height_800hPa
    hourly_data["geopotential_height_700hPa"] = hourly_geopotential_height_700hPa
    hourly_data["geopotential_height_600hPa"] = hourly_geopotential_height_600hPa
    hourly_data["geopotential_height_500hPa"] = hourly_geopotential_height_500hPa
    hourly_data["geopotential_height_400hPa"] = hourly_geopotential_height_400hPa
    hourly_data["geopotential_height_300hPa"] = hourly_geopotential_height_300hPa
    hourly_data["geopotential_height_250hPa"] = hourly_geopotential_height_250hPa
    hourly_data["geopotential_height_200hPa"] = hourly_geopotential_height_200hPa
    hourly_data["geopotential_height_150hPa"] = hourly_geopotential_height_150hPa
    hourly_data["geopotential_height_100hPa"] = hourly_geopotential_height_100hPa
    hourly_data["geopotential_height_70hPa"] = hourly_geopotential_height_70hPa
    hourly_data["geopotential_height_50hPa"] = hourly_geopotential_height_50hPa
    hourly_data["geopotential_height_30hPa"] = hourly_geopotential_height_30hPa

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    print(hourly_dataframe)
    return
