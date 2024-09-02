# config_loader.py
# This module contains functions to save and load configurations stored in json files.

import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Get or create the data directory
def get_config_dir():
    CONFIG_DIR = BASE_DIR / "config"
    CONFIG_DIR.mkdir(exist_ok=True)
    return CONFIG_DIR


# Get the config directory
DEFAULT_CONFIG_DIR = BASE_DIR / "default_config"


# Function to save configurations
def save_config(config_name, config_data):
    config_path = get_config_dir() / f"{config_name}.json"
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=4, sort_keys=True)


# Function to load configurations
def load_config(config_name):
    try:
        config_path = get_config_dir() / f"{config_name}.json"
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Function to copy a default config file to the data directory
def create_config(config_name):
    default_config_path = DEFAULT_CONFIG_DIR / f"{config_name}.json"
    config_path = get_config_dir() / f"{config_name}.json"
    with open(default_config_path, "r") as f:
        with open(config_path, "w") as g:
            g.write(f.read())
