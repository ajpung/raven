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
            "temp_1000_hPa",
            "temp_975_hPa",
            "temp_950_hPa",
            "temp_925_hPa",
            "temp_900_hPa",
            "temp_850_hPa",
            "temp_800_hPa",
            "temp_700_hPa",
            "temp_600_hPa",
            "temp_500_hPa",
            "temp_400_hPa",
            "temp_300_hPa",
            "temp_250_hPa",
            "temp_200_hPa",
            "temp_150_hPa",
            "temp_100_hPa",
            "temp_70_hPa",
            "temp_50_hPa",
            "temp_30_hPa",
            "relhum_1000_hPa",
            "relhum_975_hPa",
            "relhum_950_hPa",
            "relhum_925_hPa",
            "relhum_900_hPa",
            "relhum_850_hPa",
            "relhum_800_hPa",
            "relhum_700_hPa",
            "relhum_600_hPa",
            "relhum_500_hPa",
            "relhum_400_hPa",
            "relhum_300_hPa",
            "relhum_250_hPa",
            "relhum_200_hPa",
            "relhum_150_hPa",
            "relhum_100_hPa",
            "relhum_70_hPa",
            "relhum_50_hPa",
            "relhum_30_hPa",
            "cloud_cover_1000_hPa",
            "cloud_cover_975_hPa",
            "cloud_cover_950_hPa",
            "cloud_cover_925_hPa",
            "cloud_cover_900_hPa",
            "cloud_cover_850_hPa",
            "cloud_cover_800_hPa",
            "cloud_cover_700_hPa",
            "cloud_cover_600_hPa",
            "cloud_cover_500_hPa",
            "cloud_cover_400_hPa",
            "cloud_cover_300_hPa",
            "cloud_cover_250_hPa",
            "cloud_cover_200_hPa",
            "cloud_cover_150_hPa",
            "cloud_cover_100_hPa",
            "cloud_cover_70_hPa",
            "cloud_cover_50_hPa",
            "cloud_cover_30_hPa",
            "wind_speed_1000_hPa",
            "wind_speed_975_hPa",
            "wind_speed_950_hPa",
            "wind_speed_925_hPa",
            "wind_speed_900_hPa",
            "wind_speed_850_hPa",
            "wind_speed_800_hPa",
            "wind_speed_700_hPa",
            "wind_speed_600_hPa",
            "wind_speed_500_hPa",
            "wind_speed_400_hPa",
            "wind_speed_300_hPa",
            "wind_speed_250_hPa",
            "wind_speed_200_hPa",
            "wind_speed_150_hPa",
            "wind_speed_100_hPa",
            "wind_speed_70_hPa",
            "wind_speed_50_hPa",
            "wind_speed_30_hPa",
            "wind_direction_1000_hPa",
            "wind_direction_975_hPa",
            "wind_direction_950_hPa",
            "wind_direction_925_hPa",
            "wind_direction_900_hPa",
            "wind_direction_850_hPa",
            "wind_direction_800_hPa",
            "wind_direction_700_hPa",
            "wind_direction_600_hPa",
            "wind_direction_500_hPa",
            "wind_direction_400_hPa",
            "wind_direction_300_hPa",
            "wind_direction_250_hPa",
            "wind_direction_200_hPa",
            "wind_direction_150_hPa",
            "wind_direction_100_hPa",
            "wind_direction_70_hPa",
            "wind_direction_50_hPa",
            "wind_direction_30_hPa",
            "geopotht_1000_hPa",
            "geopotht_975_hPa",
            "geopotht_950_hPa",
            "geopotht_925_hPa",
            "geopotht_900_hPa",
            "geopotht_850_hPa",
            "geopotht_800_hPa",
            "geopotht_700_hPa",
            "geopotht_600_hPa",
            "geopotht_500_hPa",
            "geopotht_400_hPa",
            "geopotht_300_hPa",
            "geopotht_250_hPa",
            "geopotht_200_hPa",
            "geopotht_150_hPa",
            "geopotht_100_hPa",
            "geopotht_70_hPa",
            "geopotht_50_hPa",
            "geopotht_30_hPa",
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
    uv_index = hourly.Variables(0).ValuesAsNumpy()
    uv_index_clear_sky = hourly.Variables(1).ValuesAsNumpy()
    is_day = hourly.Variables(2).ValuesAsNumpy()
    sunshine_duration = hourly.Variables(3).ValuesAsNumpy()
    wet_bulb_temp_2m = hourly.Variables(4).ValuesAsNumpy()
    total_column_integrated_water_vapour = hourly.Variables(5).ValuesAsNumpy()
    cape = hourly.Variables(6).ValuesAsNumpy()
    lifted_index = hourly.Variables(7).ValuesAsNumpy()
    convective_inhibition = hourly.Variables(8).ValuesAsNumpy()
    freezing_level_height = hourly.Variables(9).ValuesAsNumpy()
    boundary_layer_height = hourly.Variables(10).ValuesAsNumpy()
    shortwave_radiation = hourly.Variables(11).ValuesAsNumpy()
    direct_radiation = hourly.Variables(12).ValuesAsNumpy()
    diffuse_radiation = hourly.Variables(13).ValuesAsNumpy()
    direct_normal_irradiance = hourly.Variables(14).ValuesAsNumpy()
    global_tilted_irradiance = hourly.Variables(15).ValuesAsNumpy()
    terrestrial_radiation = hourly.Variables(16).ValuesAsNumpy()
    shortwave_radiation_instant = hourly.Variables(17).ValuesAsNumpy()
    direct_radiation_instant = hourly.Variables(18).ValuesAsNumpy()
    diffuse_radiation_instant = hourly.Variables(19).ValuesAsNumpy()
    direct_normal_irradiance_instant = hourly.Variables(20).ValuesAsNumpy()
    global_tilted_irradiance_instant = hourly.Variables(21).ValuesAsNumpy()
    terrestrial_radiation_instant = hourly.Variables(22).ValuesAsNumpy()
    temp_1000_hPa = hourly.Variables(23).ValuesAsNumpy()
    temp_975_hPa = hourly.Variables(24).ValuesAsNumpy()
    temp_950_hPa = hourly.Variables(25).ValuesAsNumpy()
    temp_925_hPa = hourly.Variables(26).ValuesAsNumpy()
    temp_900_hPa = hourly.Variables(27).ValuesAsNumpy()
    temp_850_hPa = hourly.Variables(28).ValuesAsNumpy()
    temp_800_hPa = hourly.Variables(29).ValuesAsNumpy()
    temp_700_hPa = hourly.Variables(30).ValuesAsNumpy()
    temp_600_hPa = hourly.Variables(31).ValuesAsNumpy()
    temp_500_hPa = hourly.Variables(32).ValuesAsNumpy()
    temp_400_hPa = hourly.Variables(33).ValuesAsNumpy()
    temp_300_hPa = hourly.Variables(34).ValuesAsNumpy()
    temp_250_hPa = hourly.Variables(35).ValuesAsNumpy()
    temp_200_hPa = hourly.Variables(36).ValuesAsNumpy()
    temp_150_hPa = hourly.Variables(37).ValuesAsNumpy()
    temp_100_hPa = hourly.Variables(38).ValuesAsNumpy()
    temp_70_hPa = hourly.Variables(39).ValuesAsNumpy()
    temp_50_hPa = hourly.Variables(40).ValuesAsNumpy()
    temp_30_hPa = hourly.Variables(41).ValuesAsNumpy()
    relhum_1000_hPa = hourly.Variables(42).ValuesAsNumpy()
    relhum_975_hPa = hourly.Variables(43).ValuesAsNumpy()
    relhum_950_hPa = hourly.Variables(44).ValuesAsNumpy()
    relhum_925_hPa = hourly.Variables(45).ValuesAsNumpy()
    relhum_900_hPa = hourly.Variables(46).ValuesAsNumpy()
    relhum_850_hPa = hourly.Variables(47).ValuesAsNumpy()
    relhum_800_hPa = hourly.Variables(48).ValuesAsNumpy()
    relhum_700_hPa = hourly.Variables(49).ValuesAsNumpy()
    relhum_600_hPa = hourly.Variables(50).ValuesAsNumpy()
    relhum_500_hPa = hourly.Variables(51).ValuesAsNumpy()
    relhum_400_hPa = hourly.Variables(52).ValuesAsNumpy()
    relhum_300_hPa = hourly.Variables(53).ValuesAsNumpy()
    relhum_250_hPa = hourly.Variables(54).ValuesAsNumpy()
    relhum_200_hPa = hourly.Variables(55).ValuesAsNumpy()
    relhum_150_hPa = hourly.Variables(56).ValuesAsNumpy()
    relhum_100_hPa = hourly.Variables(57).ValuesAsNumpy()
    relhum_70_hPa = hourly.Variables(58).ValuesAsNumpy()
    relhum_50_hPa = hourly.Variables(59).ValuesAsNumpy()
    relhum_30_hPa = hourly.Variables(60).ValuesAsNumpy()
    cldcov_1000_hPa = hourly.Variables(61).ValuesAsNumpy()
    cldcov_975_hPa = hourly.Variables(62).ValuesAsNumpy()
    cldcov_950_hPa = hourly.Variables(63).ValuesAsNumpy()
    cldcov_925_hPa = hourly.Variables(64).ValuesAsNumpy()
    cldcov_900_hPa = hourly.Variables(65).ValuesAsNumpy()
    cldcov_850_hPa = hourly.Variables(66).ValuesAsNumpy()
    cldcov_800_hPa = hourly.Variables(67).ValuesAsNumpy()
    cldcov_700_hPa = hourly.Variables(68).ValuesAsNumpy()
    cldcov_600_hPa = hourly.Variables(69).ValuesAsNumpy()
    cldcov_500_hPa = hourly.Variables(70).ValuesAsNumpy()
    cldcov_400_hPa = hourly.Variables(71).ValuesAsNumpy()
    cldcov_300_hPa = hourly.Variables(72).ValuesAsNumpy()
    cldcov_250_hPa = hourly.Variables(73).ValuesAsNumpy()
    cldcov_200_hPa = hourly.Variables(74).ValuesAsNumpy()
    cldcov_150_hPa = hourly.Variables(75).ValuesAsNumpy()
    cldcov_100_hPa = hourly.Variables(76).ValuesAsNumpy()
    cldcov_70_hPa = hourly.Variables(77).ValuesAsNumpy()
    cldcov_50_hPa = hourly.Variables(78).ValuesAsNumpy()
    cldcov_30_hPa = hourly.Variables(79).ValuesAsNumpy()
    wndspd_1000_hPa = hourly.Variables(80).ValuesAsNumpy()
    wndspd_975_hPa = hourly.Variables(81).ValuesAsNumpy()
    wndspd_950_hPa = hourly.Variables(82).ValuesAsNumpy()
    wndspd_925_hPa = hourly.Variables(83).ValuesAsNumpy()
    wndspd_900_hPa = hourly.Variables(84).ValuesAsNumpy()
    wndspd_850_hPa = hourly.Variables(85).ValuesAsNumpy()
    wndspd_800_hPa = hourly.Variables(86).ValuesAsNumpy()
    wndspd_700_hPa = hourly.Variables(87).ValuesAsNumpy()
    wndspd_600_hPa = hourly.Variables(88).ValuesAsNumpy()
    wndspd_500_hPa = hourly.Variables(89).ValuesAsNumpy()
    wndspd_400_hPa = hourly.Variables(90).ValuesAsNumpy()
    wndspd_300_hPa = hourly.Variables(91).ValuesAsNumpy()
    wndspd_250_hPa = hourly.Variables(92).ValuesAsNumpy()
    wndspd_200_hPa = hourly.Variables(93).ValuesAsNumpy()
    wndspd_150_hPa = hourly.Variables(94).ValuesAsNumpy()
    wndspd_100_hPa = hourly.Variables(95).ValuesAsNumpy()
    wndspd_70_hPa = hourly.Variables(96).ValuesAsNumpy()
    wndspd_50_hPa = hourly.Variables(97).ValuesAsNumpy()
    wndspd_30_hPa = hourly.Variables(98).ValuesAsNumpy()
    wnddir_1000_hPa = hourly.Variables(99).ValuesAsNumpy()
    wnddir_975_hPa = hourly.Variables(100).ValuesAsNumpy()
    wnddir_950_hPa = hourly.Variables(101).ValuesAsNumpy()
    wnddir_925_hPa = hourly.Variables(102).ValuesAsNumpy()
    wnddir_900_hPa = hourly.Variables(103).ValuesAsNumpy()
    wnddir_850_hPa = hourly.Variables(104).ValuesAsNumpy()
    wnddir_800_hPa = hourly.Variables(105).ValuesAsNumpy()
    wnddir_700_hPa = hourly.Variables(106).ValuesAsNumpy()
    wnddir_600_hPa = hourly.Variables(107).ValuesAsNumpy()
    wnddir_500_hPa = hourly.Variables(108).ValuesAsNumpy()
    wnddir_400_hPa = hourly.Variables(109).ValuesAsNumpy()
    wnddir_300_hPa = hourly.Variables(110).ValuesAsNumpy()
    wnddir_250_hPa = hourly.Variables(111).ValuesAsNumpy()
    wnddir_200_hPa = hourly.Variables(112).ValuesAsNumpy()
    wnddir_150_hPa = hourly.Variables(113).ValuesAsNumpy()
    wnddir_100_hPa = hourly.Variables(114).ValuesAsNumpy()
    wnddir_70_hPa = hourly.Variables(115).ValuesAsNumpy()
    wnddir_50_hPa = hourly.Variables(116).ValuesAsNumpy()
    wnddir_30_hPa = hourly.Variables(117).ValuesAsNumpy()
    geopotht_1000_hPa = hourly.Variables(118).ValuesAsNumpy()
    geopotht_975_hPa = hourly.Variables(119).ValuesAsNumpy()
    geopotht_950_hPa = hourly.Variables(120).ValuesAsNumpy()
    geopotht_925_hPa = hourly.Variables(121).ValuesAsNumpy()
    geopotht_900_hPa = hourly.Variables(122).ValuesAsNumpy()
    geopotht_850_hPa = hourly.Variables(123).ValuesAsNumpy()
    geopotht_800_hPa = hourly.Variables(124).ValuesAsNumpy()
    geopotht_700_hPa = hourly.Variables(125).ValuesAsNumpy()
    geopotht_600_hPa = hourly.Variables(126).ValuesAsNumpy()
    geopotht_500_hPa = hourly.Variables(127).ValuesAsNumpy()
    geopotht_400_hPa = hourly.Variables(128).ValuesAsNumpy()
    geopotht_300_hPa = hourly.Variables(129).ValuesAsNumpy()
    geopotht_250_hPa = hourly.Variables(130).ValuesAsNumpy()
    geopotht_200_hPa = hourly.Variables(131).ValuesAsNumpy()
    geopotht_150_hPa = hourly.Variables(132).ValuesAsNumpy()
    geopotht_100_hPa = hourly.Variables(133).ValuesAsNumpy()
    geopotht_70_hPa = hourly.Variables(134).ValuesAsNumpy()
    geopotht_50_hPa = hourly.Variables(135).ValuesAsNumpy()
    geopotht_30_hPa = hourly.Variables(136).ValuesAsNumpy()

    hr_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }

    hr_data["uv_index"] = uv_index
    hr_data["uv_index_clear_sky"] = uv_index_clear_sky
    hr_data["is_day"] = is_day
    hr_data["sunshine_duration"] = sunshine_duration
    hr_data["wet_bulb_temperature_2m"] = wet_bulb_temp_2m
    hr_data["total_column_integrated_water_vapour"] = (
        total_column_integrated_water_vapour
    )
    hr_data["cape"] = cape
    hr_data["lifted_index"] = lifted_index
    hr_data["convective_inhibition"] = convective_inhibition
    hr_data["freezing_level_height"] = freezing_level_height
    hr_data["boundary_layer_height"] = boundary_layer_height
    hr_data["shortwave_radiation"] = shortwave_radiation
    hr_data["direct_radiation"] = direct_radiation
    hr_data["diffuse_radiation"] = diffuse_radiation
    hr_data["direct_normal_irradiance"] = direct_normal_irradiance
    hr_data["global_tilted_irradiance"] = global_tilted_irradiance
    hr_data["terrestrial_radiation"] = terrestrial_radiation
    hr_data["shortwave_radiation_instant"] = shortwave_radiation_instant
    hr_data["direct_radiation_instant"] = direct_radiation_instant
    hr_data["diffuse_radiation_instant"] = diffuse_radiation_instant
    hr_data["direct_normal_irradiance_instant"] = direct_normal_irradiance_instant
    hr_data["global_tilted_irradiance_instant"] = global_tilted_irradiance_instant
    hr_data["terrestrial_radiation_instant"] = terrestrial_radiation_instant
    hr_data["temp_1000_hPa"] = temp_1000_hPa
    hr_data["temp_975_hPa"] = temp_975_hPa
    hr_data["temp_950_hPa"] = temp_950_hPa
    hr_data["temp_925_hPa"] = temp_925_hPa
    hr_data["temp_900_hPa"] = temp_900_hPa
    hr_data["temp_850_hPa"] = temp_850_hPa
    hr_data["temp_800_hPa"] = temp_800_hPa
    hr_data["temp_700_hPa"] = temp_700_hPa
    hr_data["temp_600_hPa"] = temp_600_hPa
    hr_data["temp_500_hPa"] = temp_500_hPa
    hr_data["temp_400_hPa"] = temp_400_hPa
    hr_data["temp_300_hPa"] = temp_300_hPa
    hr_data["temp_250_hPa"] = temp_250_hPa
    hr_data["temp_200_hPa"] = temp_200_hPa
    hr_data["temp_150_hPa"] = temp_150_hPa
    hr_data["temp_100_hPa"] = temp_100_hPa
    hr_data["temp_70_hPa"] = temp_70_hPa
    hr_data["temp_50_hPa"] = temp_50_hPa
    hr_data["temp_30_hPa"] = temp_30_hPa
    hr_data["relhum_1000_hPa"] = relhum_1000_hPa
    hr_data["relhum_975_hPa"] = relhum_975_hPa
    hr_data["relhum_950_hPa"] = relhum_950_hPa
    hr_data["relhum_925_hPa"] = relhum_925_hPa
    hr_data["relhum_900_hPa"] = relhum_900_hPa
    hr_data["relhum_850_hPa"] = relhum_850_hPa
    hr_data["relhum_800_hPa"] = relhum_800_hPa
    hr_data["relhum_700_hPa"] = relhum_700_hPa
    hr_data["relhum_600_hPa"] = relhum_600_hPa
    hr_data["relhum_500_hPa"] = relhum_500_hPa
    hr_data["relhum_400_hPa"] = relhum_400_hPa
    hr_data["relhum_300_hPa"] = relhum_300_hPa
    hr_data["relhum_250_hPa"] = relhum_250_hPa
    hr_data["relhum_200_hPa"] = relhum_200_hPa
    hr_data["relhum_150_hPa"] = relhum_150_hPa
    hr_data["relhum_100_hPa"] = relhum_100_hPa
    hr_data["relhum_70_hPa"] = relhum_70_hPa
    hr_data["relhum_50_hPa"] = relhum_50_hPa
    hr_data["relhum_30_hPa"] = relhum_30_hPa
    hr_data["cldcov_1000_hPa"] = cldcov_1000_hPa
    hr_data["cldcov_975_hPa"] = cldcov_975_hPa
    hr_data["cldcov_950_hPa"] = cldcov_950_hPa
    hr_data["cldcov_925_hPa"] = cldcov_925_hPa
    hr_data["cldcov_900_hPa"] = cldcov_900_hPa
    hr_data["cldcov_850_hPa"] = cldcov_850_hPa
    hr_data["cldcov_800_hPa"] = cldcov_800_hPa
    hr_data["cldcov_700_hPa"] = cldcov_700_hPa
    hr_data["cldcov_600_hPa"] = cldcov_600_hPa
    hr_data["cldcov_500_hPa"] = cldcov_500_hPa
    hr_data["cldcov_400_hPa"] = cldcov_400_hPa
    hr_data["cldcov_300_hPa"] = cldcov_300_hPa
    hr_data["cldcov_250_hPa"] = cldcov_250_hPa
    hr_data["cldcov_200_hPa"] = cldcov_200_hPa
    hr_data["cldcov_150_hPa"] = cldcov_150_hPa
    hr_data["cldcov_100_hPa"] = cldcov_100_hPa
    hr_data["cldcov_70_hPa"] = cldcov_70_hPa
    hr_data["cldcov_50_hPa"] = cldcov_50_hPa
    hr_data["cldcov_30_hPa"] = cldcov_30_hPa
    hr_data["wndspd_1000_hPa"] = wndspd_1000_hPa
    hr_data["wndspd_975_hPa"] = wndspd_975_hPa
    hr_data["wndspd_950_hPa"] = wndspd_950_hPa
    hr_data["wndspd_925_hPa"] = wndspd_925_hPa
    hr_data["wndspd_900_hPa"] = wndspd_900_hPa
    hr_data["wndspd_850_hPa"] = wndspd_850_hPa
    hr_data["wndspd_800_hPa"] = wndspd_800_hPa
    hr_data["wndspd_700_hPa"] = wndspd_700_hPa
    hr_data["wndspd_600_hPa"] = wndspd_600_hPa
    hr_data["wndspd_500_hPa"] = wndspd_500_hPa
    hr_data["wndspd_400_hPa"] = wndspd_400_hPa
    hr_data["wndspd_300_hPa"] = wndspd_300_hPa
    hr_data["wndspd_250_hPa"] = wndspd_250_hPa
    hr_data["wndspd_200_hPa"] = wndspd_200_hPa
    hr_data["wndspd_150_hPa"] = wndspd_150_hPa
    hr_data["wndspd_100_hPa"] = wndspd_100_hPa
    hr_data["wndspd_70_hPa"] = wndspd_70_hPa
    hr_data["wndspd_50_hPa"] = wndspd_50_hPa
    hr_data["wndspd_30_hPa"] = wndspd_30_hPa
    hr_data["wnddir_1000_hPa"] = wnddir_1000_hPa
    hr_data["wnddir_975_hPa"] = wnddir_975_hPa
    hr_data["wnddir_950_hPa"] = wnddir_950_hPa
    hr_data["wnddir_925_hPa"] = wnddir_925_hPa
    hr_data["wnddir_900_hPa"] = wnddir_900_hPa
    hr_data["wnddir_850_hPa"] = wnddir_850_hPa
    hr_data["wnddir_800_hPa"] = wnddir_800_hPa
    hr_data["wnddir_700_hPa"] = wnddir_700_hPa
    hr_data["wnddir_600_hPa"] = wnddir_600_hPa
    hr_data["wnddir_500_hPa"] = wnddir_500_hPa
    hr_data["wnddir_400_hPa"] = wnddir_400_hPa
    hr_data["wnddir_300_hPa"] = wnddir_300_hPa
    hr_data["wnddir_250_hPa"] = wnddir_250_hPa
    hr_data["wnddir_200_hPa"] = wnddir_200_hPa
    hr_data["wnddir_150_hPa"] = wnddir_150_hPa
    hr_data["wnddir_100_hPa"] = wnddir_100_hPa
    hr_data["wnddir_70_hPa"] = wnddir_70_hPa
    hr_data["wnddir_50_hPa"] = wnddir_50_hPa
    hr_data["wnddir_30_hPa"] = wnddir_30_hPa
    hr_data["geopotht_1000_hPa"] = geopotht_1000_hPa
    hr_data["geopotht_975_hPa"] = geopotht_975_hPa
    hr_data["geopotht_950_hPa"] = geopotht_950_hPa
    hr_data["geopotht_925_hPa"] = geopotht_925_hPa
    hr_data["geopotht_900_hPa"] = geopotht_900_hPa
    hr_data["geopotht_850_hPa"] = geopotht_850_hPa
    hr_data["geopotht_800_hPa"] = geopotht_800_hPa
    hr_data["geopotht_700_hPa"] = geopotht_700_hPa
    hr_data["geopotht_600_hPa"] = geopotht_600_hPa
    hr_data["geopotht_500_hPa"] = geopotht_500_hPa
    hr_data["geopotht_400_hPa"] = geopotht_400_hPa
    hr_data["geopotht_300_hPa"] = geopotht_300_hPa
    hr_data["geopotht_250_hPa"] = geopotht_250_hPa
    hr_data["geopotht_200_hPa"] = geopotht_200_hPa
    hr_data["geopotht_150_hPa"] = geopotht_150_hPa
    hr_data["geopotht_100_hPa"] = geopotht_100_hPa
    hr_data["geopotht_70_hPa"] = geopotht_70_hPa
    hr_data["geopotht_50_hPa"] = geopotht_50_hPa
    hr_data["geopotht_30_hPa"] = geopotht_30_hPa

    hr_df = pd.DataFrame(data=hr_data)
    hr_df["latitude"] = lat
    hr_df["longitude"] = lon
    hr_df["Timezone"] = response.Timezone()
    return hr_df
