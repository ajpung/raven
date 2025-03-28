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
