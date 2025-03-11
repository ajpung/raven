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
        "Phrase":
        "Pleasant"
    }
},
"RelativeHumidity":32,
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
"UVIndex":4,
"UVIndexText":"Moderate",
"Visibility":{
    "Metric":{
    "Value":25.7,
    "Unit":"km",
    "UnitType":6
},
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

    my_keys = collect_keys()
    url = f"https://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={apikey}&q={lat}%2C{lon}"
    response = requests.get(url)
    data = cast(Dict[str, Any], response.json())
    return data


def gather_accuwx(lat: float, lon: float) -> Dict[str, Any]:
    """
    Collects weather data from Accuweather

    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return data: Weather data from Accuweather API
    """
    my_keys = collect_keys()
    apikey = my_keys["Weather"]["accu-weather"]
    # Collect location
    locationkey = gather_location(lat, lon, apikey)
    # If location key is found, collect weather data
    if locationkey != {}:
        locationkey = locationkey["Key"]
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{locationkey}?apikey={apikey}&details=true"
        response = requests.get(url)
        data = cast(Dict[str, Any], response.json())
        return data
    else:
        return {}
