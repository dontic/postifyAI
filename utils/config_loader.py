# config_loader.py
# This module contains functions to save and load configurations stored in json files.

import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Get or create the data directory
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


# Function to save configurations
def save_config(config_name, config_data):
    config_path = DATA_DIR / f"{config_name}.json"
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=4, sort_keys=True)


# Function to load configurations
def load_config(config_name):
    try:
        config_path = DATA_DIR / f"{config_name}.json"
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
