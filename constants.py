from typing import Any

import yaml

####################
# Default Settings #
####################
DEFAULT_TIMEZONE_STR = "UTC"

##########################
# Configuration Settings #
##########################
config: dict[str, Any]
try:
    with open("config.yaml", "r") as config_file:
        config = yaml.full_load(config_file)
except OSError:
    config = {}

COLLOQUIAL_USERNAME: str = config.get("colloquial_username", "streamer")
TIMEZONE: str = config.get("timezone", DEFAULT_TIMEZONE_STR)
