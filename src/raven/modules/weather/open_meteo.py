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
            "temp_1000hPa",
            "temp_975hPa",
            "temp_950hPa",
            "temp_925hPa",
            "temp_900hPa",
            "temp_850hPa",
            "temp_800hPa",
            "temp_700hPa",
            "temp_600hPa",
            "temp_500hPa",
            "temp_400hPa",
            "temp_300hPa",
            "temp_250hPa",
            "temp_200hPa",
            "temp_150hPa",
            "temp_100hPa",
            "temp_70hPa",
            "temp_50hPa",
            "temp_30hPa",
            "relhum_1000hPa",
            "relhum_975hPa",
            "relhum_950hPa",
            "relhum_925hPa",
            "relhum_900hPa",
            "relhum_850hPa",
            "relhum_800hPa",
            "relhum_700hPa",
            "relhum_600hPa",
            "relhum_500hPa",
            "relhum_400hPa",
            "relhum_300hPa",
            "relhum_250hPa",
            "relhum_200hPa",
            "relhum_150hPa",
            "relhum_100hPa",
            "relhum_70hPa",
            "relhum_50hPa",
            "relhum_30hPa",
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
            "geopotht_1000hPa",
            "geopotht_975hPa",
            "geopotht_950hPa",
            "geopotht_925hPa",
            "geopotht_900hPa",
            "geopotht_850hPa",
            "geopotht_800hPa",
            "geopotht_700hPa",
            "geopotht_600hPa",
            "geopotht_500hPa",
            "geopotht_400hPa",
            "geopotht_300hPa",
            "geopotht_250hPa",
            "geopotht_200hPa",
            "geopotht_150hPa",
            "geopotht_100hPa",
            "geopotht_70hPa",
            "geopotht_50hPa",
            "geopotht_30hPa",
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
    temp_1000hPa = hourly.Variables(23).ValuesAsNumpy()
    temp_975hPa = hourly.Variables(24).ValuesAsNumpy()
    temp_950hPa = hourly.Variables(25).ValuesAsNumpy()
    temp_925hPa = hourly.Variables(26).ValuesAsNumpy()
    temp_900hPa = hourly.Variables(27).ValuesAsNumpy()
    temp_850hPa = hourly.Variables(28).ValuesAsNumpy()
    temp_800hPa = hourly.Variables(29).ValuesAsNumpy()
    temp_700hPa = hourly.Variables(30).ValuesAsNumpy()
    temp_600hPa = hourly.Variables(31).ValuesAsNumpy()
    temp_500hPa = hourly.Variables(32).ValuesAsNumpy()
    temp_400hPa = hourly.Variables(33).ValuesAsNumpy()
    temp_300hPa = hourly.Variables(34).ValuesAsNumpy()
    temp_250hPa = hourly.Variables(35).ValuesAsNumpy()
    temp_200hPa = hourly.Variables(36).ValuesAsNumpy()
    temp_150hPa = hourly.Variables(37).ValuesAsNumpy()
    temp_100hPa = hourly.Variables(38).ValuesAsNumpy()
    temp_70hPa = hourly.Variables(39).ValuesAsNumpy()
    temp_50hPa = hourly.Variables(40).ValuesAsNumpy()
    temp_30hPa = hourly.Variables(41).ValuesAsNumpy()
    relhum_1000hPa = hourly.Variables(42).ValuesAsNumpy()
    relhum_975hPa = hourly.Variables(43).ValuesAsNumpy()
    relhum_950hPa = hourly.Variables(44).ValuesAsNumpy()
    relhum_925hPa = hourly.Variables(45).ValuesAsNumpy()
    relhum_900hPa = hourly.Variables(46).ValuesAsNumpy()
    relhum_850hPa = hourly.Variables(47).ValuesAsNumpy()
    relhum_800hPa = hourly.Variables(48).ValuesAsNumpy()
    relhum_700hPa = hourly.Variables(49).ValuesAsNumpy()
    relhum_600hPa = hourly.Variables(50).ValuesAsNumpy()
    relhum_500hPa = hourly.Variables(51).ValuesAsNumpy()
    relhum_400hPa = hourly.Variables(52).ValuesAsNumpy()
    relhum_300hPa = hourly.Variables(53).ValuesAsNumpy()
    relhum_250hPa = hourly.Variables(54).ValuesAsNumpy()
    relhum_200hPa = hourly.Variables(55).ValuesAsNumpy()
    relhum_150hPa = hourly.Variables(56).ValuesAsNumpy()
    relhum_100hPa = hourly.Variables(57).ValuesAsNumpy()
    relhum_70hPa = hourly.Variables(58).ValuesAsNumpy()
    relhum_50hPa = hourly.Variables(59).ValuesAsNumpy()
    relhum_30hPa = hourly.Variables(60).ValuesAsNumpy()
    cldcov_1000hPa = hourly.Variables(61).ValuesAsNumpy()
    cldcov_975hPa = hourly.Variables(62).ValuesAsNumpy()
    cldcov_950hPa = hourly.Variables(63).ValuesAsNumpy()
    cldcov_925hPa = hourly.Variables(64).ValuesAsNumpy()
    cldcov_900hPa = hourly.Variables(65).ValuesAsNumpy()
    cldcov_850hPa = hourly.Variables(66).ValuesAsNumpy()
    cldcov_800hPa = hourly.Variables(67).ValuesAsNumpy()
    cldcov_700hPa = hourly.Variables(68).ValuesAsNumpy()
    cldcov_600hPa = hourly.Variables(69).ValuesAsNumpy()
    cldcov_500hPa = hourly.Variables(70).ValuesAsNumpy()
    cldcov_400hPa = hourly.Variables(71).ValuesAsNumpy()
    cldcov_300hPa = hourly.Variables(72).ValuesAsNumpy()
    cldcov_250hPa = hourly.Variables(73).ValuesAsNumpy()
    cldcov_200hPa = hourly.Variables(74).ValuesAsNumpy()
    cldcov_150hPa = hourly.Variables(75).ValuesAsNumpy()
    cldcov_100hPa = hourly.Variables(76).ValuesAsNumpy()
    cldcov_70hPa = hourly.Variables(77).ValuesAsNumpy()
    cldcov_50hPa = hourly.Variables(78).ValuesAsNumpy()
    cldcov_30hPa = hourly.Variables(79).ValuesAsNumpy()
    wndspd_1000hPa = hourly.Variables(80).ValuesAsNumpy()
    wndspd_975hPa = hourly.Variables(81).ValuesAsNumpy()
    wndspd_950hPa = hourly.Variables(82).ValuesAsNumpy()
    wndspd_925hPa = hourly.Variables(83).ValuesAsNumpy()
    wndspd_900hPa = hourly.Variables(84).ValuesAsNumpy()
    wndspd_850hPa = hourly.Variables(85).ValuesAsNumpy()
    wndspd_800hPa = hourly.Variables(86).ValuesAsNumpy()
    wndspd_700hPa = hourly.Variables(87).ValuesAsNumpy()
    wndspd_600hPa = hourly.Variables(88).ValuesAsNumpy()
    wndspd_500hPa = hourly.Variables(89).ValuesAsNumpy()
    wndspd_400hPa = hourly.Variables(90).ValuesAsNumpy()
    wndspd_300hPa = hourly.Variables(91).ValuesAsNumpy()
    wndspd_250hPa = hourly.Variables(92).ValuesAsNumpy()
    wndspd_200hPa = hourly.Variables(93).ValuesAsNumpy()
    wndspd_150hPa = hourly.Variables(94).ValuesAsNumpy()
    wndspd_100hPa = hourly.Variables(95).ValuesAsNumpy()
    wndspd_70hPa = hourly.Variables(96).ValuesAsNumpy()
    wndspd_50hPa = hourly.Variables(97).ValuesAsNumpy()
    wndspd_30hPa = hourly.Variables(98).ValuesAsNumpy()
    wnddir_1000hPa = hourly.Variables(99).ValuesAsNumpy()
    wnddir_975hPa = hourly.Variables(100).ValuesAsNumpy()
    wnddir_950hPa = hourly.Variables(101).ValuesAsNumpy()
    wnddir_925hPa = hourly.Variables(102).ValuesAsNumpy()
    wnddir_900hPa = hourly.Variables(103).ValuesAsNumpy()
    wnddir_850hPa = hourly.Variables(104).ValuesAsNumpy()
    wnddir_800hPa = hourly.Variables(105).ValuesAsNumpy()
    wnddir_700hPa = hourly.Variables(106).ValuesAsNumpy()
    wnddir_600hPa = hourly.Variables(107).ValuesAsNumpy()
    wnddir_500hPa = hourly.Variables(108).ValuesAsNumpy()
    wnddir_400hPa = hourly.Variables(109).ValuesAsNumpy()
    wnddir_300hPa = hourly.Variables(110).ValuesAsNumpy()
    wnddir_250hPa = hourly.Variables(111).ValuesAsNumpy()
    wnddir_200hPa = hourly.Variables(112).ValuesAsNumpy()
    wnddir_150hPa = hourly.Variables(113).ValuesAsNumpy()
    wnddir_100hPa = hourly.Variables(114).ValuesAsNumpy()
    wnddir_70hPa = hourly.Variables(115).ValuesAsNumpy()
    wnddir_50hPa = hourly.Variables(116).ValuesAsNumpy()
    wnddir_30hPa = hourly.Variables(117).ValuesAsNumpy()
    geopotht_1000hPa = hourly.Variables(118).ValuesAsNumpy()
    geopotht_975hPa = hourly.Variables(119).ValuesAsNumpy()
    geopotht_950hPa = hourly.Variables(120).ValuesAsNumpy()
    geopotht_925hPa = hourly.Variables(121).ValuesAsNumpy()
    geopotht_900hPa = hourly.Variables(122).ValuesAsNumpy()
    geopotht_850hPa = hourly.Variables(123).ValuesAsNumpy()
    geopotht_800hPa = hourly.Variables(124).ValuesAsNumpy()
    geopotht_700hPa = hourly.Variables(125).ValuesAsNumpy()
    geopotht_600hPa = hourly.Variables(126).ValuesAsNumpy()
    geopotht_500hPa = hourly.Variables(127).ValuesAsNumpy()
    geopotht_400hPa = hourly.Variables(128).ValuesAsNumpy()
    geopotht_300hPa = hourly.Variables(129).ValuesAsNumpy()
    geopotht_250hPa = hourly.Variables(130).ValuesAsNumpy()
    geopotht_200hPa = hourly.Variables(131).ValuesAsNumpy()
    geopotht_150hPa = hourly.Variables(132).ValuesAsNumpy()
    geopotht_100hPa = hourly.Variables(133).ValuesAsNumpy()
    geopotht_70hPa = hourly.Variables(134).ValuesAsNumpy()
    geopotht_50hPa = hourly.Variables(135).ValuesAsNumpy()
    geopotht_30hPa = hourly.Variables(136).ValuesAsNumpy()

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
    hr_data["temp_1000hPa"] = temp_1000hPa
    hr_data["temp_975hPa"] = temp_975hPa
    hr_data["temp_950hPa"] = temp_950hPa
    hr_data["temp_925hPa"] = temp_925hPa
    hr_data["temp_900hPa"] = temp_900hPa
    hr_data["temp_850hPa"] = temp_850hPa
    hr_data["temp_800hPa"] = temp_800hPa
    hr_data["temp_700hPa"] = temp_700hPa
    hr_data["temp_600hPa"] = temp_600hPa
    hr_data["temp_500hPa"] = temp_500hPa
    hr_data["temp_400hPa"] = temp_400hPa
    hr_data["temp_300hPa"] = temp_300hPa
    hr_data["temp_250hPa"] = temp_250hPa
    hr_data["temp_200hPa"] = temp_200hPa
    hr_data["temp_150hPa"] = temp_150hPa
    hr_data["temp_100hPa"] = temp_100hPa
    hr_data["temp_70hPa"] = temp_70hPa
    hr_data["temp_50hPa"] = temp_50hPa
    hr_data["temp_30hPa"] = temp_30hPa
    hr_data["relhum_1000hPa"] = relhum_1000hPa
    hr_data["relhum_975hPa"] = relhum_975hPa
    hr_data["relhum_950hPa"] = relhum_950hPa
    hr_data["relhum_925hPa"] = relhum_925hPa
    hr_data["relhum_900hPa"] = relhum_900hPa
    hr_data["relhum_850hPa"] = relhum_850hPa
    hr_data["relhum_800hPa"] = relhum_800hPa
    hr_data["relhum_700hPa"] = relhum_700hPa
    hr_data["relhum_600hPa"] = relhum_600hPa
    hr_data["relhum_500hPa"] = relhum_500hPa
    hr_data["relhum_400hPa"] = relhum_400hPa
    hr_data["relhum_300hPa"] = relhum_300hPa
    hr_data["relhum_250hPa"] = relhum_250hPa
    hr_data["relhum_200hPa"] = relhum_200hPa
    hr_data["relhum_150hPa"] = relhum_150hPa
    hr_data["relhum_100hPa"] = relhum_100hPa
    hr_data["relhum_70hPa"] = relhum_70hPa
    hr_data["relhum_50hPa"] = relhum_50hPa
    hr_data["relhum_30hPa"] = relhum_30hPa
    hr_data["cldcov_1000hPa"] = cldcov_1000hPa
    hr_data["cldcov_975hPa"] = cldcov_975hPa
    hr_data["cldcov_950hPa"] = cldcov_950hPa
    hr_data["cldcov_925hPa"] = cldcov_925hPa
    hr_data["cldcov_900hPa"] = cldcov_900hPa
    hr_data["cldcov_850hPa"] = cldcov_850hPa
    hr_data["cldcov_800hPa"] = cldcov_800hPa
    hr_data["cldcov_700hPa"] = cldcov_700hPa
    hr_data["cldcov_600hPa"] = cldcov_600hPa
    hr_data["cldcov_500hPa"] = cldcov_500hPa
    hr_data["cldcov_400hPa"] = cldcov_400hPa
    hr_data["cldcov_300hPa"] = cldcov_300hPa
    hr_data["cldcov_250hPa"] = cldcov_250hPa
    hr_data["cldcov_200hPa"] = cldcov_200hPa
    hr_data["cldcov_150hPa"] = cldcov_150hPa
    hr_data["cldcov_100hPa"] = cldcov_100hPa
    hr_data["cldcov_70hPa"] = cldcov_70hPa
    hr_data["cldcov_50hPa"] = cldcov_50hPa
    hr_data["cldcov_30hPa"] = cldcov_30hPa
    hr_data["wndspd_1000hPa"] = wndspd_1000hPa
    hr_data["wndspd_975hPa"] = wndspd_975hPa
    hr_data["wndspd_950hPa"] = wndspd_950hPa
    hr_data["wndspd_925hPa"] = wndspd_925hPa
    hr_data["wndspd_900hPa"] = wndspd_900hPa
    hr_data["wndspd_850hPa"] = wndspd_850hPa
    hr_data["wndspd_800hPa"] = wndspd_800hPa
    hr_data["wndspd_700hPa"] = wndspd_700hPa
    hr_data["wndspd_600hPa"] = wndspd_600hPa
    hr_data["wndspd_500hPa"] = wndspd_500hPa
    hr_data["wndspd_400hPa"] = wndspd_400hPa
    hr_data["wndspd_300hPa"] = wndspd_300hPa
    hr_data["wndspd_250hPa"] = wndspd_250hPa
    hr_data["wndspd_200hPa"] = wndspd_200hPa
    hr_data["wndspd_150hPa"] = wndspd_150hPa
    hr_data["wndspd_100hPa"] = wndspd_100hPa
    hr_data["wndspd_70hPa"] = wndspd_70hPa
    hr_data["wndspd_50hPa"] = wndspd_50hPa
    hr_data["wndspd_30hPa"] = wndspd_30hPa
    hr_data["wnddir_1000hPa"] = wnddir_1000hPa
    hr_data["wnddir_975hPa"] = wnddir_975hPa
    hr_data["wnddir_950hPa"] = wnddir_950hPa
    hr_data["wnddir_925hPa"] = wnddir_925hPa
    hr_data["wnddir_900hPa"] = wnddir_900hPa
    hr_data["wnddir_850hPa"] = wnddir_850hPa
    hr_data["wnddir_800hPa"] = wnddir_800hPa
    hr_data["wnddir_700hPa"] = wnddir_700hPa
    hr_data["wnddir_600hPa"] = wnddir_600hPa
    hr_data["wnddir_500hPa"] = wnddir_500hPa
    hr_data["wnddir_400hPa"] = wnddir_400hPa
    hr_data["wnddir_300hPa"] = wnddir_300hPa
    hr_data["wnddir_250hPa"] = wnddir_250hPa
    hr_data["wnddir_200hPa"] = wnddir_200hPa
    hr_data["wnddir_150hPa"] = wnddir_150hPa
    hr_data["wnddir_100hPa"] = wnddir_100hPa
    hr_data["wnddir_70hPa"] = wnddir_70hPa
    hr_data["wnddir_50hPa"] = wnddir_50hPa
    hr_data["wnddir_30hPa"] = wnddir_30hPa
    hr_data["geopotht_1000hPa"] = geopotht_1000hPa
    hr_data["geopotht_975hPa"] = geopotht_975hPa
    hr_data["geopotht_950hPa"] = geopotht_950hPa
    hr_data["geopotht_925hPa"] = geopotht_925hPa
    hr_data["geopotht_900hPa"] = geopotht_900hPa
    hr_data["geopotht_850hPa"] = geopotht_850hPa
    hr_data["geopotht_800hPa"] = geopotht_800hPa
    hr_data["geopotht_700hPa"] = geopotht_700hPa
    hr_data["geopotht_600hPa"] = geopotht_600hPa
    hr_data["geopotht_500hPa"] = geopotht_500hPa
    hr_data["geopotht_400hPa"] = geopotht_400hPa
    hr_data["geopotht_300hPa"] = geopotht_300hPa
    hr_data["geopotht_250hPa"] = geopotht_250hPa
    hr_data["geopotht_200hPa"] = geopotht_200hPa
    hr_data["geopotht_150hPa"] = geopotht_150hPa
    hr_data["geopotht_100hPa"] = geopotht_100hPa
    hr_data["geopotht_70hPa"] = geopotht_70hPa
    hr_data["geopotht_50hPa"] = geopotht_50hPa
    hr_data["geopotht_30hPa"] = geopotht_30hPa

    hr_df = pd.DataFrame(data=hr_data)
    hr_df["latitude"] = lat
    hr_df["longitude"] = lon
    hr_df["Timezone"] = response.Timezone()
    return hr_df
