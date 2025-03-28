import numpy as np
import pandas as pd
from geopy import distance  # type: ignore
from raven.core.file_io import find_indices_of_length_one


def _parse_airport_locations(
    filepath: str = "../docs/_static/stations.txt",
) -> pd.DataFrame:
    """
    Parse airport locations from a METAR file.

    :param filepath: Path to airport locations file
    :return: DataFrame with airport locations
    """
    # Read / open METAR file
    with open(filepath, "r") as file:
        lines = file.readlines()

    # Eliminate header
    data = lines[44:]

    # Identify rows without useful data
    indices = find_indices_of_length_one(data)
    indices += [indices[i] + 1 for i in np.arange(len(indices))]
    indices += [indices[i] + 1 for i in np.arange(len(indices))]
    sort_idx = sorted(indices)

    # Delete rows at elements
    data = [item for i, item in enumerate(data) if i not in sort_idx]

    # Parse relevant information from strings
    iata = [data[i][26:29] for i in np.arange(len(data) - 1)]
    syno = [data[i][32:37] for i in np.arange(len(data) - 1)]
    clat = [
        data[i][39:45].split(" ")[0] + "." + data[i][39:45].split(" ")[1]
        for i in np.arange(len(data) - 1)
    ]
    lati = [float(x[:-1]) if x[-1] == "N" else -float(x[:-1]) for x in clat]
    clon = [
        data[i][47:54].split(" ")[0] + "." + data[i][47:54].split(" ")[1]
        for i in np.arange(len(data) - 1)
    ]
    long = [float(x[:-1]) if x[-1] == "E" else -float(x[:-1]) for x in clon]
    elev = [data[i][56:60] for i in np.arange(len(data) - 1)]

    # Generate dataframe
    data_df = pd.DataFrame(
        {
            "IATA": iata,
            "Synop": syno,
            "Latitude": lati,
            "Longitude": long,
            "Elevation": elev,
        }
    )

    return data_df


def find_airport_distances(lat: float, lon: float) -> pd.DataFrame:
    """
    Find distances to airports from a given location.

    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return: DataFrame with distances to airports
    """
    # Extract airport locations
    data_df = _parse_airport_locations()

    # Calculate distances to all airports
    data_df["Distance"] = data_df.apply(
        lambda row: distance.geodesic(
            (lat, lon), (row["Latitude"], row["Longitude"])
        ).km,
        axis=1,
    )

    # Sort by distance
    data_df = data_df.sort_values(by="Distance")

    return data_df


def find_five_nearest(lat: float, lon: float, data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Find the five nearest airports to a given location.

    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :param data_df: DataFrame with airport locations
    :return: DataFrame with five nearest airports
    """
    # Find distances to all airports
    data_df = find_airport_distances(lat, lon)

    # Select the five nearest airports
    nearest_airports = data_df.iloc[:5]

    return nearest_airports
