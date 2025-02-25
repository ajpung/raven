from typing import Any, Dict, Tuple

import openmeteo_requests  # type: ignore
import pandas as pd
import requests_cache
from retry_requests import retry  # type: ignore
from pandas import DataFrame

"""
Units taken from https://open-meteo.com/en/docs

__Clouds__
Altitude: km
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
Humidity: % 
Rain: mm
Showers: mm
Ice accum: 
Intensity: 
Probability: %
Type: 
Evapotranspiration: mm
Total precip: mm

__Pressure__
Sea Level: hPa 
Surface Level: hPa 

__Radiation__
Shortwave: W/m^2
Direct: W/m^2
Diffuse: W/m^2
Global tilted irradiance: W/m^2

__Soil__
Moisture (Volumetric): m^3/m^3 
Temperature: C 

__Solar__
DIF: 
DIR: 
GHI: 

__Snow__
Accumulation: cm
Depth: m

__Swells__
(Primary & Secondary)
Direction: 
Mean Period: 
Significant Height: 

__Temp__
Dewpoint: C 
Temp: C
Apparent: C 

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
visibility: m 

__Weeds__
weedGrassIndex: 
WeedIndex: 

__Waves__
SignificantHeight: 
Direction: 
MeanPeriod: 

__Wind__
Speed: km/h
Gust: km/h
Direction: degrees 
windWaveSignificantHeight: 
windWaveDirection: 
windWaveMeanPeriod: 
"""


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
            "temp_1000hpa",
            "temp_975hpa",
            "temp_950hpa",
            "temp_925hpa",
            "temp_900hpa",
            "temp_850hpa",
            "temp_800hpa",
            "temp_700hpa",
            "temp_600hpa",
            "temp_500hpa",
            "temp_400hpa",
            "temp_300hpa",
            "temp_250hpa",
            "temp_200hpa",
            "temp_150hpa",
            "temp_100hpa",
            "temp_70hpa",
            "temp_50hpa",
            "temp_30hpa",
            "relhum_1000hpa",
            "relhum_975hpa",
            "relhum_950hpa",
            "relhum_925hpa",
            "relhum_900hpa",
            "relhum_850hpa",
            "relhum_800hpa",
            "relhum_700hpa",
            "relhum_600hpa",
            "relhum_500hpa",
            "relhum_400hpa",
            "relhum_300hpa",
            "relhum_250hpa",
            "relhum_200hpa",
            "relhum_150hpa",
            "relhum_100hpa",
            "relhum_70hpa",
            "relhum_50hpa",
            "relhum_30hpa",
            "cloud_cover_1000hpa",
            "cloud_cover_975hpa",
            "cloud_cover_950hpa",
            "cloud_cover_925hpa",
            "cloud_cover_900hpa",
            "cloud_cover_850hpa",
            "cloud_cover_800hpa",
            "cloud_cover_700hpa",
            "cloud_cover_600hpa",
            "cloud_cover_500hpa",
            "cloud_cover_400hpa",
            "cloud_cover_300hpa",
            "cloud_cover_250hpa",
            "cloud_cover_200hpa",
            "cloud_cover_150hpa",
            "cloud_cover_100hpa",
            "cloud_cover_70hpa",
            "cloud_cover_50hpa",
            "cloud_cover_30hpa",
            "wind_speed_1000hpa",
            "wind_speed_975hpa",
            "wind_speed_950hpa",
            "wind_speed_925hpa",
            "wind_speed_900hpa",
            "wind_speed_850hpa",
            "wind_speed_800hpa",
            "wind_speed_700hpa",
            "wind_speed_600hpa",
            "wind_speed_500hpa",
            "wind_speed_400hpa",
            "wind_speed_300hpa",
            "wind_speed_250hpa",
            "wind_speed_200hpa",
            "wind_speed_150hpa",
            "wind_speed_100hpa",
            "wind_speed_70hpa",
            "wind_speed_50hpa",
            "wind_speed_30hpa",
            "wind_direction_1000hpa",
            "wind_direction_975hpa",
            "wind_direction_950hpa",
            "wind_direction_925hpa",
            "wind_direction_900hpa",
            "wind_direction_850hpa",
            "wind_direction_800hpa",
            "wind_direction_700hpa",
            "wind_direction_600hpa",
            "wind_direction_500hpa",
            "wind_direction_400hpa",
            "wind_direction_300hpa",
            "wind_direction_250hpa",
            "wind_direction_200hpa",
            "wind_direction_150hpa",
            "wind_direction_100hpa",
            "wind_direction_70hpa",
            "wind_direction_50hpa",
            "wind_direction_30hpa",
            "geopotht_1000hpa",
            "geopotht_975hpa",
            "geopotht_950hpa",
            "geopotht_925hpa",
            "geopotht_900hpa",
            "geopotht_850hpa",
            "geopotht_800hpa",
            "geopotht_700hpa",
            "geopotht_600hpa",
            "geopotht_500hpa",
            "geopotht_400hpa",
            "geopotht_300hpa",
            "geopotht_250hpa",
            "geopotht_200hpa",
            "geopotht_150hpa",
            "geopotht_100hpa",
            "geopotht_70hpa",
            "geopotht_50hpa",
            "geopotht_30hpa",
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
    temp_1000hpa = hourly.Variables(23).ValuesAsNumpy()
    temp_975hpa = hourly.Variables(24).ValuesAsNumpy()
    temp_950hpa = hourly.Variables(25).ValuesAsNumpy()
    temp_925hpa = hourly.Variables(26).ValuesAsNumpy()
    temp_900hpa = hourly.Variables(27).ValuesAsNumpy()
    temp_850hpa = hourly.Variables(28).ValuesAsNumpy()
    temp_800hpa = hourly.Variables(29).ValuesAsNumpy()
    temp_700hpa = hourly.Variables(30).ValuesAsNumpy()
    temp_600hpa = hourly.Variables(31).ValuesAsNumpy()
    temp_500hpa = hourly.Variables(32).ValuesAsNumpy()
    temp_400hpa = hourly.Variables(33).ValuesAsNumpy()
    temp_300hpa = hourly.Variables(34).ValuesAsNumpy()
    temp_250hpa = hourly.Variables(35).ValuesAsNumpy()
    temp_200hpa = hourly.Variables(36).ValuesAsNumpy()
    temp_150hpa = hourly.Variables(37).ValuesAsNumpy()
    temp_100hpa = hourly.Variables(38).ValuesAsNumpy()
    temp_70hpa = hourly.Variables(39).ValuesAsNumpy()
    temp_50hpa = hourly.Variables(40).ValuesAsNumpy()
    temp_30hpa = hourly.Variables(41).ValuesAsNumpy()
    relhum_1000hpa = hourly.Variables(42).ValuesAsNumpy()
    relhum_975hpa = hourly.Variables(43).ValuesAsNumpy()
    relhum_950hpa = hourly.Variables(44).ValuesAsNumpy()
    relhum_925hpa = hourly.Variables(45).ValuesAsNumpy()
    relhum_900hpa = hourly.Variables(46).ValuesAsNumpy()
    relhum_850hpa = hourly.Variables(47).ValuesAsNumpy()
    relhum_800hpa = hourly.Variables(48).ValuesAsNumpy()
    relhum_700hpa = hourly.Variables(49).ValuesAsNumpy()
    relhum_600hpa = hourly.Variables(50).ValuesAsNumpy()
    relhum_500hpa = hourly.Variables(51).ValuesAsNumpy()
    relhum_400hpa = hourly.Variables(52).ValuesAsNumpy()
    relhum_300hpa = hourly.Variables(53).ValuesAsNumpy()
    relhum_250hpa = hourly.Variables(54).ValuesAsNumpy()
    relhum_200hpa = hourly.Variables(55).ValuesAsNumpy()
    relhum_150hpa = hourly.Variables(56).ValuesAsNumpy()
    relhum_100hpa = hourly.Variables(57).ValuesAsNumpy()
    relhum_70hpa = hourly.Variables(58).ValuesAsNumpy()
    relhum_50hpa = hourly.Variables(59).ValuesAsNumpy()
    relhum_30hpa = hourly.Variables(60).ValuesAsNumpy()
    cldcov_1000hpa = hourly.Variables(61).ValuesAsNumpy()
    cldcov_975hpa = hourly.Variables(62).ValuesAsNumpy()
    cldcov_950hpa = hourly.Variables(63).ValuesAsNumpy()
    cldcov_925hpa = hourly.Variables(64).ValuesAsNumpy()
    cldcov_900hpa = hourly.Variables(65).ValuesAsNumpy()
    cldcov_850hpa = hourly.Variables(66).ValuesAsNumpy()
    cldcov_800hpa = hourly.Variables(67).ValuesAsNumpy()
    cldcov_700hpa = hourly.Variables(68).ValuesAsNumpy()
    cldcov_600hpa = hourly.Variables(69).ValuesAsNumpy()
    cldcov_500hpa = hourly.Variables(70).ValuesAsNumpy()
    cldcov_400hpa = hourly.Variables(71).ValuesAsNumpy()
    cldcov_300hpa = hourly.Variables(72).ValuesAsNumpy()
    cldcov_250hpa = hourly.Variables(73).ValuesAsNumpy()
    cldcov_200hpa = hourly.Variables(74).ValuesAsNumpy()
    cldcov_150hpa = hourly.Variables(75).ValuesAsNumpy()
    cldcov_100hpa = hourly.Variables(76).ValuesAsNumpy()
    cldcov_70hpa = hourly.Variables(77).ValuesAsNumpy()
    cldcov_50hpa = hourly.Variables(78).ValuesAsNumpy()
    cldcov_30hpa = hourly.Variables(79).ValuesAsNumpy()
    wndspd_1000hpa = hourly.Variables(80).ValuesAsNumpy()
    wndspd_975hpa = hourly.Variables(81).ValuesAsNumpy()
    wndspd_950hpa = hourly.Variables(82).ValuesAsNumpy()
    wndspd_925hpa = hourly.Variables(83).ValuesAsNumpy()
    wndspd_900hpa = hourly.Variables(84).ValuesAsNumpy()
    wndspd_850hpa = hourly.Variables(85).ValuesAsNumpy()
    wndspd_800hpa = hourly.Variables(86).ValuesAsNumpy()
    wndspd_700hpa = hourly.Variables(87).ValuesAsNumpy()
    wndspd_600hpa = hourly.Variables(88).ValuesAsNumpy()
    wndspd_500hpa = hourly.Variables(89).ValuesAsNumpy()
    wndspd_400hpa = hourly.Variables(90).ValuesAsNumpy()
    wndspd_300hpa = hourly.Variables(91).ValuesAsNumpy()
    wndspd_250hpa = hourly.Variables(92).ValuesAsNumpy()
    wndspd_200hpa = hourly.Variables(93).ValuesAsNumpy()
    wndspd_150hpa = hourly.Variables(94).ValuesAsNumpy()
    wndspd_100hpa = hourly.Variables(95).ValuesAsNumpy()
    wndspd_70hpa = hourly.Variables(96).ValuesAsNumpy()
    wndspd_50hpa = hourly.Variables(97).ValuesAsNumpy()
    wndspd_30hpa = hourly.Variables(98).ValuesAsNumpy()
    wnddir_1000hpa = hourly.Variables(99).ValuesAsNumpy()
    wnddir_975hpa = hourly.Variables(100).ValuesAsNumpy()
    wnddir_950hpa = hourly.Variables(101).ValuesAsNumpy()
    wnddir_925hpa = hourly.Variables(102).ValuesAsNumpy()
    wnddir_900hpa = hourly.Variables(103).ValuesAsNumpy()
    wnddir_850hpa = hourly.Variables(104).ValuesAsNumpy()
    wnddir_800hpa = hourly.Variables(105).ValuesAsNumpy()
    wnddir_700hpa = hourly.Variables(106).ValuesAsNumpy()
    wnddir_600hpa = hourly.Variables(107).ValuesAsNumpy()
    wnddir_500hpa = hourly.Variables(108).ValuesAsNumpy()
    wnddir_400hpa = hourly.Variables(109).ValuesAsNumpy()
    wnddir_300hpa = hourly.Variables(110).ValuesAsNumpy()
    wnddir_250hpa = hourly.Variables(111).ValuesAsNumpy()
    wnddir_200hpa = hourly.Variables(112).ValuesAsNumpy()
    wnddir_150hpa = hourly.Variables(113).ValuesAsNumpy()
    wnddir_100hpa = hourly.Variables(114).ValuesAsNumpy()
    wnddir_70hpa = hourly.Variables(115).ValuesAsNumpy()
    wnddir_50hpa = hourly.Variables(116).ValuesAsNumpy()
    wnddir_30hpa = hourly.Variables(117).ValuesAsNumpy()
    geopotht_1000hpa = hourly.Variables(118).ValuesAsNumpy()
    geopotht_975hpa = hourly.Variables(119).ValuesAsNumpy()
    geopotht_950hpa = hourly.Variables(120).ValuesAsNumpy()
    geopotht_925hpa = hourly.Variables(121).ValuesAsNumpy()
    geopotht_900hpa = hourly.Variables(122).ValuesAsNumpy()
    geopotht_850hpa = hourly.Variables(123).ValuesAsNumpy()
    geopotht_800hpa = hourly.Variables(124).ValuesAsNumpy()
    geopotht_700hpa = hourly.Variables(125).ValuesAsNumpy()
    geopotht_600hpa = hourly.Variables(126).ValuesAsNumpy()
    geopotht_500hpa = hourly.Variables(127).ValuesAsNumpy()
    geopotht_400hpa = hourly.Variables(128).ValuesAsNumpy()
    geopotht_300hpa = hourly.Variables(129).ValuesAsNumpy()
    geopotht_250hpa = hourly.Variables(130).ValuesAsNumpy()
    geopotht_200hpa = hourly.Variables(131).ValuesAsNumpy()
    geopotht_150hpa = hourly.Variables(132).ValuesAsNumpy()
    geopotht_100hpa = hourly.Variables(133).ValuesAsNumpy()
    geopotht_70hpa = hourly.Variables(134).ValuesAsNumpy()
    geopotht_50hpa = hourly.Variables(135).ValuesAsNumpy()
    geopotht_30hpa = hourly.Variables(136).ValuesAsNumpy()

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
    hr_data["temp_1000hpa"] = temp_1000hpa
    hr_data["temp_975hpa"] = temp_975hpa
    hr_data["temp_950hpa"] = temp_950hpa
    hr_data["temp_925hpa"] = temp_925hpa
    hr_data["temp_900hpa"] = temp_900hpa
    hr_data["temp_850hpa"] = temp_850hpa
    hr_data["temp_800hpa"] = temp_800hpa
    hr_data["temp_700hpa"] = temp_700hpa
    hr_data["temp_600hpa"] = temp_600hpa
    hr_data["temp_500hpa"] = temp_500hpa
    hr_data["temp_400hpa"] = temp_400hpa
    hr_data["temp_300hpa"] = temp_300hpa
    hr_data["temp_250hpa"] = temp_250hpa
    hr_data["temp_200hpa"] = temp_200hpa
    hr_data["temp_150hpa"] = temp_150hpa
    hr_data["temp_100hpa"] = temp_100hpa
    hr_data["temp_70hpa"] = temp_70hpa
    hr_data["temp_50hpa"] = temp_50hpa
    hr_data["temp_30hpa"] = temp_30hpa
    hr_data["relhum_1000hpa"] = relhum_1000hpa
    hr_data["relhum_975hpa"] = relhum_975hpa
    hr_data["relhum_950hpa"] = relhum_950hpa
    hr_data["relhum_925hpa"] = relhum_925hpa
    hr_data["relhum_900hpa"] = relhum_900hpa
    hr_data["relhum_850hpa"] = relhum_850hpa
    hr_data["relhum_800hpa"] = relhum_800hpa
    hr_data["relhum_700hpa"] = relhum_700hpa
    hr_data["relhum_600hpa"] = relhum_600hpa
    hr_data["relhum_500hpa"] = relhum_500hpa
    hr_data["relhum_400hpa"] = relhum_400hpa
    hr_data["relhum_300hpa"] = relhum_300hpa
    hr_data["relhum_250hpa"] = relhum_250hpa
    hr_data["relhum_200hpa"] = relhum_200hpa
    hr_data["relhum_150hpa"] = relhum_150hpa
    hr_data["relhum_100hpa"] = relhum_100hpa
    hr_data["relhum_70hpa"] = relhum_70hpa
    hr_data["relhum_50hpa"] = relhum_50hpa
    hr_data["relhum_30hpa"] = relhum_30hpa
    hr_data["cldcov_1000hpa"] = cldcov_1000hpa
    hr_data["cldcov_975hpa"] = cldcov_975hpa
    hr_data["cldcov_950hpa"] = cldcov_950hpa
    hr_data["cldcov_925hpa"] = cldcov_925hpa
    hr_data["cldcov_900hpa"] = cldcov_900hpa
    hr_data["cldcov_850hpa"] = cldcov_850hpa
    hr_data["cldcov_800hpa"] = cldcov_800hpa
    hr_data["cldcov_700hpa"] = cldcov_700hpa
    hr_data["cldcov_600hpa"] = cldcov_600hpa
    hr_data["cldcov_500hpa"] = cldcov_500hpa
    hr_data["cldcov_400hpa"] = cldcov_400hpa
    hr_data["cldcov_300hpa"] = cldcov_300hpa
    hr_data["cldcov_250hpa"] = cldcov_250hpa
    hr_data["cldcov_200hpa"] = cldcov_200hpa
    hr_data["cldcov_150hpa"] = cldcov_150hpa
    hr_data["cldcov_100hpa"] = cldcov_100hpa
    hr_data["cldcov_70hpa"] = cldcov_70hpa
    hr_data["cldcov_50hpa"] = cldcov_50hpa
    hr_data["cldcov_30hpa"] = cldcov_30hpa
    hr_data["wndspd_1000hpa"] = wndspd_1000hpa
    hr_data["wndspd_975hpa"] = wndspd_975hpa
    hr_data["wndspd_950hpa"] = wndspd_950hpa
    hr_data["wndspd_925hpa"] = wndspd_925hpa
    hr_data["wndspd_900hpa"] = wndspd_900hpa
    hr_data["wndspd_850hpa"] = wndspd_850hpa
    hr_data["wndspd_800hpa"] = wndspd_800hpa
    hr_data["wndspd_700hpa"] = wndspd_700hpa
    hr_data["wndspd_600hpa"] = wndspd_600hpa
    hr_data["wndspd_500hpa"] = wndspd_500hpa
    hr_data["wndspd_400hpa"] = wndspd_400hpa
    hr_data["wndspd_300hpa"] = wndspd_300hpa
    hr_data["wndspd_250hpa"] = wndspd_250hpa
    hr_data["wndspd_200hpa"] = wndspd_200hpa
    hr_data["wndspd_150hpa"] = wndspd_150hpa
    hr_data["wndspd_100hpa"] = wndspd_100hpa
    hr_data["wndspd_70hpa"] = wndspd_70hpa
    hr_data["wndspd_50hpa"] = wndspd_50hpa
    hr_data["wndspd_30hpa"] = wndspd_30hpa
    hr_data["wnddir_1000hpa"] = wnddir_1000hpa
    hr_data["wnddir_975hpa"] = wnddir_975hpa
    hr_data["wnddir_950hpa"] = wnddir_950hpa
    hr_data["wnddir_925hpa"] = wnddir_925hpa
    hr_data["wnddir_900hpa"] = wnddir_900hpa
    hr_data["wnddir_850hpa"] = wnddir_850hpa
    hr_data["wnddir_800hpa"] = wnddir_800hpa
    hr_data["wnddir_700hpa"] = wnddir_700hpa
    hr_data["wnddir_600hpa"] = wnddir_600hpa
    hr_data["wnddir_500hpa"] = wnddir_500hpa
    hr_data["wnddir_400hpa"] = wnddir_400hpa
    hr_data["wnddir_300hpa"] = wnddir_300hpa
    hr_data["wnddir_250hpa"] = wnddir_250hpa
    hr_data["wnddir_200hpa"] = wnddir_200hpa
    hr_data["wnddir_150hpa"] = wnddir_150hpa
    hr_data["wnddir_100hpa"] = wnddir_100hpa
    hr_data["wnddir_70hpa"] = wnddir_70hpa
    hr_data["wnddir_50hpa"] = wnddir_50hpa
    hr_data["wnddir_30hpa"] = wnddir_30hpa
    hr_data["geopotht_1000hpa"] = geopotht_1000hpa
    hr_data["geopotht_975hpa"] = geopotht_975hpa
    hr_data["geopotht_950hpa"] = geopotht_950hpa
    hr_data["geopotht_925hpa"] = geopotht_925hpa
    hr_data["geopotht_900hpa"] = geopotht_900hpa
    hr_data["geopotht_850hpa"] = geopotht_850hpa
    hr_data["geopotht_800hpa"] = geopotht_800hpa
    hr_data["geopotht_700hpa"] = geopotht_700hpa
    hr_data["geopotht_600hpa"] = geopotht_600hpa
    hr_data["geopotht_500hpa"] = geopotht_500hpa
    hr_data["geopotht_400hpa"] = geopotht_400hpa
    hr_data["geopotht_300hpa"] = geopotht_300hpa
    hr_data["geopotht_250hpa"] = geopotht_250hpa
    hr_data["geopotht_200hpa"] = geopotht_200hpa
    hr_data["geopotht_150hpa"] = geopotht_150hpa
    hr_data["geopotht_100hpa"] = geopotht_100hpa
    hr_data["geopotht_70hpa"] = geopotht_70hpa
    hr_data["geopotht_50hpa"] = geopotht_50hpa
    hr_data["geopotht_30hpa"] = geopotht_30hpa

    hr_df = pd.DataFrame(data=hr_data)
    hr_df["latitude"] = lat
    hr_df["longitude"] = lon
    hr_df["Timezone"] = response.Timezone()
    return hr_df
