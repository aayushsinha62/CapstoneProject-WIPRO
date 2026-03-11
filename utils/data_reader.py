"""
Data Reader Utility

Reads test data from CSV files and converts it into a format
compatible with pytest parameterization.
"""

import pandas as pd
from utils.paths import PROJECT_ROOT


def get_test_data(file):
    """
    Load test data from a CSV file.

    Parameters
    ----------
    file : str
        Relative path to the CSV file from project root.

    Returns
    -------
    list
        List of rows containing test data for pytest parametrization.
    """

    # Build absolute path to CSV file
    file_path = PROJECT_ROOT / file

    # Read CSV data
    df = pd.read_csv(file_path, encoding="utf-8")

    # Replace NaN values with empty strings and convert to list
    return df.fillna("").values.tolist()