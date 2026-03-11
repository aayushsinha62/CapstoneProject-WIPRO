"""
Configuration Reader

Provides utility functions to load framework configuration
settings from the JSON configuration file.

The configuration file stores environment-specific parameters such as:
- Base URL
- Browser type
- Implicit wait
- Explicit wait

Using centralized configuration allows the framework behavior
to be modified without changing the test or framework code.
"""

import json
from utils.paths import PROJECT_ROOT

def get_config():
    """
    Load and return configuration settings from config.json.

    Returns
    -------
    dict
        Dictionary containing framework configuration values.
    """

    # Build absolute path to configuration file
    config_path = PROJECT_ROOT / "config" / "config.json"

    # Read and parse JSON configuration
    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    return config