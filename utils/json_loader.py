# json_loader.py
# This module contains functions to save and load json files.

# Imports
import json
from pathlib import Path

# Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Function to save json files
def save_json(filepath, data):
    """
    Save a json file with the given data

    Args:
        filepath (str): The path to the file, relative to the root directory
        data (dict): The data to save in the file

    Returns:
        None
    """
    # Disect the path
    path = BASE_DIR / filepath

    # Ensure the directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Ensure the data is a dictionary or a list
    if not isinstance(data, (dict, list)):
        raise ValueError("Data must be a dictionary or a list")

    # Save the data
    with open(path, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)


# Function to load json files
def load_json(filepath):
    """
    Function to load a json file

    Args:
        filepath (str): The path to the file, relative to the root directory

    Returns:
        dict | list: The data in the json file
    """

    # Disect the path
    path = BASE_DIR / filepath

    # Ensure the file exists
    if not path.exists():
        raise FileNotFoundError(f"File {path} not found")

    # Load the data
    with open(path, "r") as f:
        return json.load(f)
