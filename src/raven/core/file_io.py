import numpy as np
import pandas as pd


def find_indices_of_length_one(data: list) -> list:
    """
    Finds the indices of elements with length 1 in a list.

    Args:
        data: A list of elements (strings, lists, etc.).

    Returns:
        A list of indices where elements have length 1.
    """
    indices = []
    for index, element in enumerate(data):
        try:
            if len(element) == 1:
                indices.append(index)
        except TypeError:
            # Handle cases where len() is not applicable (e.g., for integers)
            continue
    return indices


def parse_airport_locations(
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
