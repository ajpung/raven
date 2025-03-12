import datetime
import json
from typing import Dict, Any, cast

import openmeteo_requests  # type: ignore
import requests
from raven.core.api_base import collect_keys
from pandas import DataFrame
from retry_requests import retry

"""
Units taken from:
    (location) https://developer.accuweather.com/accuweather-locations-api/apis/get/locations/v1/cities/geoposition/search
    (weather) https://developer.accuweather.com/accuweather-current-conditions-api/apis/get/currentconditions/v1/%7BlocationKey%7D

------------------------------------------------------
!                     LOCATION                       !
------------------------------------------------------
Version: int,
Key: "2168954",
Type: "City",
Rank: 85,
LocalizedName: "Ochlocknee",
EnglishName: "Ochlocknee",
PrimaryPostalCode: "31773",
Region: {
    ID: "NAM",
    LocalizedName: "North America",
    EnglishName: "North America"
},
"Country": {
    "ID": "US",
    "LocalizedName": "United States",
    "EnglishName": "United States"
},
"AdministrativeArea": {
    "ID": "GA",
    "LocalizedName": "Georgia",
    "EnglishName": "Georgia",
    "Level": 1,
    "LocalizedType": "State",
    "EnglishType": "State",
    "CountryID": "US"
},
"TimeZone": {
    "Code": "EDT",
    "Name": "America/New_York",
    "GmtOffset": -4,
    "IsDaylightSaving": true,
    "NextOffsetChange": "2025-11-02T06:00:00Z"
},
"GeoPosition": {
    "Latitude": 30.974,
    "Longitude": -84.053,
    "Elevation": {
        "Metric": {
            "Value": 92,
            "Unit": "m",
            "UnitType": 5
        },
    }
},
  "IsAlias": false,
  "SupplementalAdminAreas": [
    {
      "Level": 2,
      "LocalizedName": "Thomas",
      "EnglishName": "Thomas"
    }
  ],
  "DataSets": [
    "AirQualityCurrentConditions",
    "AirQualityForecasts",
    "Alerts",
    "DailyAirQualityForecast",
    "DailyPollenForecast",
    "ForecastConfidence",
    "FutureRadar",
    "MinuteCast",
    "ProximityNotification-Lightning",
    "Radar"
  ]
}

------------------------------------------------------
!                      WEATHER                       !
------------------------------------------------------
"LocalObservationDateTime":"2025-03-11T14:38:00-04:00",
"EpochTime":1741718280,
"WeatherText":"Sunny",
"WeatherIcon":1,
"HasPrecipitation":false,
"PrecipitationType":null,
"IsDayTime":true,
"Temperature":{
    "Metric":{
        "Value":21.0,
        "Unit":"C",
        "UnitType":17
    },
},
"RealFeelTemperature":{
    "Metric":{
        "Value":24.4,
        "Unit":"C",
        "UnitType":17,
        "Phrase":"Pleasant"
    }
},
"RealFeelTemperatureShade":{
    "Metric":{
        "Value":19.8,
        "Unit":"C",
        "UnitType":17,
        "Phrase": "Pleasant"
    }
},
"RelativeHumidity":32,       # %
"IndoorRelativeHumidity":32,
"DewPoint":{
    "Metric":{
        "Value":3.6,
        "Unit":"C",
        "UnitType":17
    }
},
"Wind":{
    "Direction":{
        "Degrees":315,
        "Localized":"NW",
        "English":"NW"
    },
    "Speed":{
        "Metric":{
            "Value":7.0,
            "Unit":"km/h",
            "UnitType":7
        }
    }
},
"WindGust":{
    "Speed":{
        "Metric":{
            "Value":14.8,
            "Unit":"km/h"
            "UnitType":7
        }
    }
},
"Visibility":{
    "Metric":{
        "Value":25.7,
        "Unit":"km",
        "UnitType":6
    },
}
"UVIndex":4,
"UVIndexText":"Moderate",
"ObstructionsToVisibility":"",
"CloudCover":0,
"Ceiling":{
    "Metric":{
        "Value":12192.0,
        "Unit":"m",
        "UnitType":5
    },
},
"Pressure":{
    "Metric":{
        "Value":1016.3
        "Unit":"mb"
        "UnitType":14
    }
}
"PressureTendency":{
    "LocalizedText":"Falling"
    "Code":"F"
}
"Past24HourTemperatureDeparture":{
    "Metric":{
        "Value":7.5,
        "Unit":"C"
        "UnitType":17
    }
},
"ApparentTemperature":{
    "Metric":{
        "Value":20.6,
        "Unit":"C",
        "UnitType":17
    }
},
"WindChillTemperature":{
    "Metric":{
        "Value":21.1,
        "Unit":"C",
        "UnitType":17
    }
},
"WetBulbTemperature":{
    "Metric":{
        "Value":11.7
        "Unit":"C"
        "UnitType":17
    }
},
"WetBulbGlobeTemperature":{
    "Metric":{
        "Value":18.3,
        "Unit":"C",
        "UnitType":17
    }
}
"Precip1hr":{
    "Metric":{
        "Value":0.0,
        "Unit":"mm",
        "UnitType":3
    }
},
"PrecipitationSummary":{
    "Precipitation":{
        "Metric":{
            "Value":0.0,
            "Unit":"mm",
            "UnitType":3
        }
    },
    "PastHour":{
        "Metric":{
            "Value":0.0,
            "Unit":"mm",
            "UnitType":3
        },
    },
    "Past3Hours":{
        "Metric":{
            "Value":0.0,
            "Unit":"mm",
            "UnitType":3
        },
    },
    "Past6Hours":{
        "Metric":{
            "Value":0.0,
            "Unit":"mm",
            "UnitType":3
        },
    },
    "Past9Hours":{
        "Metric":{
            "Value":0.0,
            "Unit":"mm",
            "UnitType":3
        }
    },
    "Past12Hours":{
        "Metric":{
            "Value":0.0,
            "Unit":"mm",
            "UnitType":3
        },
    },
    "Past18Hours":{
        "Metric":{
            "Value":0.0,
            "Unit":"mm",
            "UnitType":3
        },
    },
    "Past24Hours":{
        "Metric":{
            "Value":0.0,
            "Unit":"mm",
            "UnitType":3
        },
    }
},
"TemperatureSummary":{
    "Past6HourRange":{
        "Minimum":{
            "Metric":{
                "Value":9.0,
                "Unit":"C",
                "UnitType":17
            },
        },
        "Maximum":{
            "Metric":{
                "Value":21.0,
                "Unit":"C",
                "UnitType":17
            },
        }
    },
    "Past12HourRange":{
        "Minimum":{
            "Metric":{
                "Value":7.5,
                "Unit":"C",
                "UnitType":17
            },
        },
        "Maximum":{
            "Metric":{
                "Value":21.0,
                "Unit":"C",
                "UnitType":17
            },
        }
    },
    "Past24HourRange":{
        "Minimum":{
            "Metric":{
                "Value":7.5,
                "Unit":"C",
                "UnitType":17
            },
        }
        "Maximum":{
            "Metric":{
                "Value":21.0,
                "Unit":"C",
                "UnitType":17
            },
        }
    }
}
"""


def gather_location(lat: float, lon: float, apikey: str) -> Dict[str, Any]:
    """
    Collects location data from Accuweather

    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :param apikey: Accuweather API key
    :return: Location data from Accuweather API
    """

    url = f"https://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={apikey}&q={lat}%2C{lon}"
    response = requests.get(url)
    data = cast(Dict[str, Any], response.json())
    return data


def gather_accuwx(lat: float, lon: float) -> dict[str, Any]:
    """
    Collects weather data from Accuweather

    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return data: Weather data from Accuweather API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["accu-weather"]
    # Collect location
    loc_data = gather_location(lat, lon, apikey)
    # If location key is found, collect weather data
    if loc_data != {}:
        locationkey = loc_data["Key"]
        url = f"https://dataservice.accuweather.com/currentconditions/v1/{locationkey}?apikey={apikey}&details=true"
        response = requests.get(url)
        data = cast(Dict[str, Any], response.json())
        data["latitude"] = loc_data["GeoPosition"]["Latitude"]
        data["longitude"] = loc_data["GeoPosition"]["Longitude"]
        data["altitude"] = loc_data["GeoPosition"]["Elevation"]["Metric"]["Value"]
    else:
        data = {}
    return data


def correct_accuwx(data: Dict[str, Any]) -> tuple[dict[str, Any], str, str, int]:
    """
    Corrects the data from AccuWeather (units, date/time)
    :param wx_data: Weather data from AccuWeather API
    :return: Corrected weather data
    """
    if data != {}:
        # Apply Unit Corrections
        # (cloud altitude, m -> km)
        data["Ceiling"]["Metric"]["Value"] = data["Ceiling"]["Metric"]["Value"] / 1000

        # Convert datetime to epoch using DateTime
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        # Parse the string to datetime object
        datetime_obj = datetime.datetime.strptime(
            data["LocalObservationDateTime"], date_format
        )
        # Extracte date and time
        date = datetime_obj.date().strftime("%Y-%m-%d")
        time = datetime_obj.time().strftime("%H:%M:%S")
        # Convert to UTC epoch
        utc_epoch = int(datetime_obj.timestamp())
    else:
        date = ""
        time = ""
        utc_epoch = 0
    return data, date, time, utc_epoch


def fill_accuwx(
    data: dict[str, Any],
    date: str,
    time: str,
    utc_epoch: int,
    json_file: str = "../docs/_static/json_template.json",
) -> dict[str, Any]:
    """
    Fills the JSON template with the data from AccuWeather
    :param data: Weather data from AccuWeather API
    :param date: Date in API request
    :param time: Time in API request
    :param utc_epoch: Epoch time in API request
    :param json_file: JSON template file
    :return: JSON template filled with data from AccuWeather
    """
    # ----- Read / fill JSON template -----
    accu_dict = json.load(open(json_file))

    # Handle case where location is not found
    if data == {}:
        return accu_dict  # type: ignore
    else:
        # Datetime
        accu_dict["datetime"]["date"] = date
        accu_dict["datetime"]["time"] = time
        accu_dict["datetime"]["epoch"] = utc_epoch
        # Location
        accu_dict["location"]["latitutde"] = data["latitude"]
        accu_dict["location"]["longitutde"] = data["longitude"]
        accu_dict["location"]["altitude"] = data["altitude"]
        # Clouds
        accu_dict["data"]["clouds"]["ceiling"] = data["Ceiling"]["Metric"]["Value"]
        accu_dict["data"]["clouds"]["cover"] = data["CloudCover"]
        # Health
        accu_dict["data"]["health"]["uv_index"] = data["UVIndex"]
        # Precipitation
        accu_dict["data"]["precipitation"]["rain"]["accumulated"] = data[
            "PrecipitationSummary"
        ]["Precipitation"]["Metric"]["Value"]
        # Temp
        accu_dict["data"]["temperature"]["dewpoint"] = data["DewPoint"]["Metric"][
            "Value"
        ]
        accu_dict["data"]["temperature"]["humidity"] = data["RelativeHumidity"]
        accu_dict["data"]["temperature"]["measured"] = data["Temperature"]["Metric"][
            "Value"
        ]
        accu_dict["data"]["temperature"]["apparent"] = data["RealFeelTemperature"][
            "Metric"
        ]["Value"]
        accu_dict["data"]["temperature"]["wetbulb"] = data["WetBulbTemperature"][
            "Metric"
        ]["Value"]
        # Pressure
        accu_dict["data"]["pressure"]["sea_level"] = data["Pressure"]["Metric"]["Value"]
        # Visibility
        accu_dict["data"]["visibility"] = data["Visibility"]["Metric"]["Value"]
        # Weather code
        accu_dict["data"]["code"] = data["data"]["values"]["weatherCode"]
        # Wind
        accu_dict["data"]["wind"]["direction"] = data["Wind"]["Direction"]["Degrees"]
        accu_dict["data"]["wind"]["gust"] = data["WindGust"]["Speed"]["Metric"]["Value"]
        accu_dict["data"]["wind"]["speed"] = data["Wind"]["Speed"]["Metric"]["Value"]
        return accu_dict  # type: ignore


def collect_accuwx(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects, corrects, and formats weather data from AccuWeather
    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return tmrw_dict: Weather data from AccuWeather API
    """
    # Collect data from API
    data = gather_accuwx(lat, lon)
    # Correct data
    data, date, time, utc_epoch = correct_accuwx(data)
    # Fill JSON template
    accu_dict = fill_accuwx(data, date, time, utc_epoch)
    return accu_dict
