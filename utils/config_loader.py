# config_loader.py
# This module contains functions to save and load configurations stored in json files.

import json
from pathlib import Path
import shutil

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
    config_path = get_config_dir() / f"{config_name}.json"
    default_config_path = DEFAULT_CONFIG_DIR / f"{config_name}.json"

    if not config_path.exists():
        if default_config_path.exists():
            shutil.copy(default_config_path, config_path)
        else:
            return {}

    with open(config_path, "r") as f:
        return json.load(f)


# Function to ensure all default configs are present
def ensure_default_configs():
    config_dir = get_config_dir()
    for default_config in DEFAULT_CONFIG_DIR.glob("*.json"):
        config_file = config_dir / default_config.name
        if not config_file.exists():
            shutil.copy(default_config, config_file)


# Call this function at the start of your application
ensure_default_configs()
