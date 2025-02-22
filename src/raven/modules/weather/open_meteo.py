from typing import Any, Dict, Tuple

import openmeteo_requests  # type: ignore
import pandas as pd
import requests_cache
from retry_requests import retry  # type: ignore
from pandas import DataFrame


def collect_openmt(lat: float, lon: float) -> Tuple[float, float, Any]:
    """
    Collects weather data from Open-Meteo API.

    Parameters
    ----------
    lat : float
        Latitude of the location.
    lon : float
        Longitude of the location.

    Returns
    -------
    Dict[str, Any]
        Weather data from Open-Meteo API.
    """

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
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
        "hourly": [
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
    return lat, lon, response


def collect_openmet_current(lat: float, lon: float) -> Dict[str, Any]:
    # Collect data
    lat, lon, response = collect_openmt(lat, lon)
    current = response.Current()
    # Parse data
    current_data = {
        "temperature": current.Variables(0).Value(),
        "relative_humidity": current.Variables(1).Value(),
        "apparent_temperature": current.Variables(2).Value(),
        "is_day": current.Variables(3).Value(),
        "precipitation": current.Variables(4).Value(),
        "rain": current.Variables(5).Value(),
        "showers": current.Variables(6).Value(),
        "snowfall": current.Variables(7).Value(),
        "wx_code": current.Variables(8).Value(),
        "cloud_cover": current.Variables(9).Value(),
        "pressure_msl": current.Variables(10).Value(),
        "surface_pressure": current.Variables(11).Value(),
        "wind_speed_10m": current.Variables(12).Value(),
        "wind_direction_10m": current.Variables(13).Value(),
        "wind_gusts_10m": current.Variables(14).Value(),
    }
    return current_data


def process_openmet_hourly(lat: float, lon: float) -> DataFrame:
    # Collect hourly data
    lat, lon, response = collect_openmt(lat, lon)
    hourly = response.Hourly()

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly_uv_index = hourly.Variables(0).ValuesAsNumpy()
    hourly_uv_index_clear_sky = hourly.Variables(1).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(2).ValuesAsNumpy()
    hourly_sunshine_duration = hourly.Variables(3).ValuesAsNumpy()
    hourly_wet_bulb_temperature_2m = hourly.Variables(4).ValuesAsNumpy()
    hourly_total_column_integrated_water_vapour = hourly.Variables(5).ValuesAsNumpy()
    hourly_cape = hourly.Variables(6).ValuesAsNumpy()
    hourly_lifted_index = hourly.Variables(7).ValuesAsNumpy()
    hourly_convective_inhibition = hourly.Variables(8).ValuesAsNumpy()
    hourly_freezing_level_height = hourly.Variables(9).ValuesAsNumpy()
    hourly_boundary_layer_height = hourly.Variables(10).ValuesAsNumpy()
    hourly_shortwave_radiation = hourly.Variables(11).ValuesAsNumpy()
    hourly_direct_radiation = hourly.Variables(12).ValuesAsNumpy()
    hourly_diffuse_radiation = hourly.Variables(13).ValuesAsNumpy()
    hourly_direct_normal_irradiance = hourly.Variables(14).ValuesAsNumpy()
    hourly_global_tilted_irradiance = hourly.Variables(15).ValuesAsNumpy()
    hourly_terrestrial_radiation = hourly.Variables(16).ValuesAsNumpy()
    hourly_shortwave_radiation_instant = hourly.Variables(17).ValuesAsNumpy()
    hourly_direct_radiation_instant = hourly.Variables(18).ValuesAsNumpy()
    hourly_diffuse_radiation_instant = hourly.Variables(19).ValuesAsNumpy()
    hourly_direct_normal_irradiance_instant = hourly.Variables(20).ValuesAsNumpy()
    hourly_global_tilted_irradiance_instant = hourly.Variables(21).ValuesAsNumpy()
    hourly_terrestrial_radiation_instant = hourly.Variables(22).ValuesAsNumpy()
    hourly_temperature_1000hPa = hourly.Variables(23).ValuesAsNumpy()
    hourly_temperature_975hPa = hourly.Variables(24).ValuesAsNumpy()
    hourly_temperature_950hPa = hourly.Variables(25).ValuesAsNumpy()
    hourly_temperature_925hPa = hourly.Variables(26).ValuesAsNumpy()
    hourly_temperature_900hPa = hourly.Variables(27).ValuesAsNumpy()
    hourly_temperature_850hPa = hourly.Variables(28).ValuesAsNumpy()
    hourly_temperature_800hPa = hourly.Variables(29).ValuesAsNumpy()
    hourly_temperature_700hPa = hourly.Variables(30).ValuesAsNumpy()
    hourly_temperature_600hPa = hourly.Variables(31).ValuesAsNumpy()
    hourly_temperature_500hPa = hourly.Variables(32).ValuesAsNumpy()
    hourly_temperature_400hPa = hourly.Variables(33).ValuesAsNumpy()
    hourly_temperature_300hPa = hourly.Variables(34).ValuesAsNumpy()
    hourly_temperature_250hPa = hourly.Variables(35).ValuesAsNumpy()
    hourly_temperature_200hPa = hourly.Variables(36).ValuesAsNumpy()
    hourly_temperature_150hPa = hourly.Variables(37).ValuesAsNumpy()
    hourly_temperature_100hPa = hourly.Variables(38).ValuesAsNumpy()
    hourly_temperature_70hPa = hourly.Variables(39).ValuesAsNumpy()
    hourly_temperature_50hPa = hourly.Variables(40).ValuesAsNumpy()
    hourly_temperature_30hPa = hourly.Variables(41).ValuesAsNumpy()
    hourly_relative_humidity_1000hPa = hourly.Variables(42).ValuesAsNumpy()
    hourly_relative_humidity_975hPa = hourly.Variables(43).ValuesAsNumpy()
    hourly_relative_humidity_950hPa = hourly.Variables(44).ValuesAsNumpy()
    hourly_relative_humidity_925hPa = hourly.Variables(45).ValuesAsNumpy()
    hourly_relative_humidity_900hPa = hourly.Variables(46).ValuesAsNumpy()
    hourly_relative_humidity_850hPa = hourly.Variables(47).ValuesAsNumpy()
    hourly_relative_humidity_800hPa = hourly.Variables(48).ValuesAsNumpy()
    hourly_relative_humidity_700hPa = hourly.Variables(49).ValuesAsNumpy()
    hourly_relative_humidity_600hPa = hourly.Variables(50).ValuesAsNumpy()
    hourly_relative_humidity_500hPa = hourly.Variables(51).ValuesAsNumpy()
    hourly_relative_humidity_400hPa = hourly.Variables(52).ValuesAsNumpy()
    hourly_relative_humidity_300hPa = hourly.Variables(53).ValuesAsNumpy()
    hourly_relative_humidity_250hPa = hourly.Variables(54).ValuesAsNumpy()
    hourly_relative_humidity_200hPa = hourly.Variables(55).ValuesAsNumpy()
    hourly_relative_humidity_150hPa = hourly.Variables(56).ValuesAsNumpy()
    hourly_relative_humidity_100hPa = hourly.Variables(57).ValuesAsNumpy()
    hourly_relative_humidity_70hPa = hourly.Variables(58).ValuesAsNumpy()
    hourly_relative_humidity_50hPa = hourly.Variables(59).ValuesAsNumpy()
    hourly_relative_humidity_30hPa = hourly.Variables(60).ValuesAsNumpy()
    hourly_cloud_cover_1000hPa = hourly.Variables(61).ValuesAsNumpy()
    hourly_cloud_cover_975hPa = hourly.Variables(62).ValuesAsNumpy()
    hourly_cloud_cover_950hPa = hourly.Variables(63).ValuesAsNumpy()
    hourly_cloud_cover_925hPa = hourly.Variables(64).ValuesAsNumpy()
    hourly_cloud_cover_900hPa = hourly.Variables(65).ValuesAsNumpy()
    hourly_cloud_cover_850hPa = hourly.Variables(66).ValuesAsNumpy()
    hourly_cloud_cover_800hPa = hourly.Variables(67).ValuesAsNumpy()
    hourly_cloud_cover_700hPa = hourly.Variables(68).ValuesAsNumpy()
    hourly_cloud_cover_600hPa = hourly.Variables(69).ValuesAsNumpy()
    hourly_cloud_cover_500hPa = hourly.Variables(70).ValuesAsNumpy()
    hourly_cloud_cover_400hPa = hourly.Variables(71).ValuesAsNumpy()
    hourly_cloud_cover_300hPa = hourly.Variables(72).ValuesAsNumpy()
    hourly_cloud_cover_250hPa = hourly.Variables(73).ValuesAsNumpy()
    hourly_cloud_cover_200hPa = hourly.Variables(74).ValuesAsNumpy()
    hourly_cloud_cover_150hPa = hourly.Variables(75).ValuesAsNumpy()
    hourly_cloud_cover_100hPa = hourly.Variables(76).ValuesAsNumpy()
    hourly_cloud_cover_70hPa = hourly.Variables(77).ValuesAsNumpy()
    hourly_cloud_cover_50hPa = hourly.Variables(78).ValuesAsNumpy()
    hourly_cloud_cover_30hPa = hourly.Variables(79).ValuesAsNumpy()
    hourly_wind_speed_1000hPa = hourly.Variables(80).ValuesAsNumpy()
    hourly_wind_speed_975hPa = hourly.Variables(81).ValuesAsNumpy()
    hourly_wind_speed_950hPa = hourly.Variables(82).ValuesAsNumpy()
    hourly_wind_speed_925hPa = hourly.Variables(83).ValuesAsNumpy()
    hourly_wind_speed_900hPa = hourly.Variables(84).ValuesAsNumpy()
    hourly_wind_speed_850hPa = hourly.Variables(85).ValuesAsNumpy()
    hourly_wind_speed_800hPa = hourly.Variables(86).ValuesAsNumpy()
    hourly_wind_speed_700hPa = hourly.Variables(87).ValuesAsNumpy()
    hourly_wind_speed_600hPa = hourly.Variables(88).ValuesAsNumpy()
    hourly_wind_speed_500hPa = hourly.Variables(89).ValuesAsNumpy()
    hourly_wind_speed_400hPa = hourly.Variables(90).ValuesAsNumpy()
    hourly_wind_speed_300hPa = hourly.Variables(91).ValuesAsNumpy()
    hourly_wind_speed_250hPa = hourly.Variables(92).ValuesAsNumpy()
    hourly_wind_speed_200hPa = hourly.Variables(93).ValuesAsNumpy()
    hourly_wind_speed_150hPa = hourly.Variables(94).ValuesAsNumpy()
    hourly_wind_speed_100hPa = hourly.Variables(95).ValuesAsNumpy()
    hourly_wind_speed_70hPa = hourly.Variables(96).ValuesAsNumpy()
    hourly_wind_speed_50hPa = hourly.Variables(97).ValuesAsNumpy()
    hourly_wind_speed_30hPa = hourly.Variables(98).ValuesAsNumpy()
    hourly_wind_direction_1000hPa = hourly.Variables(99).ValuesAsNumpy()
    hourly_wind_direction_975hPa = hourly.Variables(100).ValuesAsNumpy()
    hourly_wind_direction_950hPa = hourly.Variables(101).ValuesAsNumpy()
    hourly_wind_direction_925hPa = hourly.Variables(102).ValuesAsNumpy()
    hourly_wind_direction_900hPa = hourly.Variables(103).ValuesAsNumpy()
    hourly_wind_direction_850hPa = hourly.Variables(104).ValuesAsNumpy()
    hourly_wind_direction_800hPa = hourly.Variables(105).ValuesAsNumpy()
    hourly_wind_direction_700hPa = hourly.Variables(106).ValuesAsNumpy()
    hourly_wind_direction_600hPa = hourly.Variables(107).ValuesAsNumpy()
    hourly_wind_direction_500hPa = hourly.Variables(108).ValuesAsNumpy()
    hourly_wind_direction_400hPa = hourly.Variables(109).ValuesAsNumpy()
    hourly_wind_direction_300hPa = hourly.Variables(110).ValuesAsNumpy()
    hourly_wind_direction_250hPa = hourly.Variables(111).ValuesAsNumpy()
    hourly_wind_direction_200hPa = hourly.Variables(112).ValuesAsNumpy()
    hourly_wind_direction_150hPa = hourly.Variables(113).ValuesAsNumpy()
    hourly_wind_direction_100hPa = hourly.Variables(114).ValuesAsNumpy()
    hourly_wind_direction_70hPa = hourly.Variables(115).ValuesAsNumpy()
    hourly_wind_direction_50hPa = hourly.Variables(116).ValuesAsNumpy()
    hourly_wind_direction_30hPa = hourly.Variables(117).ValuesAsNumpy()
    hourly_geopotential_height_1000hPa = hourly.Variables(118).ValuesAsNumpy()
    hourly_geopotential_height_975hPa = hourly.Variables(119).ValuesAsNumpy()
    hourly_geopotential_height_950hPa = hourly.Variables(120).ValuesAsNumpy()
    hourly_geopotential_height_925hPa = hourly.Variables(121).ValuesAsNumpy()
    hourly_geopotential_height_900hPa = hourly.Variables(122).ValuesAsNumpy()
    hourly_geopotential_height_850hPa = hourly.Variables(123).ValuesAsNumpy()
    hourly_geopotential_height_800hPa = hourly.Variables(124).ValuesAsNumpy()
    hourly_geopotential_height_700hPa = hourly.Variables(125).ValuesAsNumpy()
    hourly_geopotential_height_600hPa = hourly.Variables(126).ValuesAsNumpy()
    hourly_geopotential_height_500hPa = hourly.Variables(127).ValuesAsNumpy()
    hourly_geopotential_height_400hPa = hourly.Variables(128).ValuesAsNumpy()
    hourly_geopotential_height_300hPa = hourly.Variables(129).ValuesAsNumpy()
    hourly_geopotential_height_250hPa = hourly.Variables(130).ValuesAsNumpy()
    hourly_geopotential_height_200hPa = hourly.Variables(131).ValuesAsNumpy()
    hourly_geopotential_height_150hPa = hourly.Variables(132).ValuesAsNumpy()
    hourly_geopotential_height_100hPa = hourly.Variables(133).ValuesAsNumpy()
    hourly_geopotential_height_70hPa = hourly.Variables(134).ValuesAsNumpy()
    hourly_geopotential_height_50hPa = hourly.Variables(135).ValuesAsNumpy()
    hourly_geopotential_height_30hPa = hourly.Variables(136).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }

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
    hourly_dataframe["latitude"] = lat
    hourly_dataframe["longitude"] = lon
    hourly_dataframe["Timezone"] = response.Timezone()
    return hourly_dataframe
