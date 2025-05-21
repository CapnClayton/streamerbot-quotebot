import pytz
import yaml

####################
# Default Settings #
####################
DEFAULT_TIMEZONE_STR = "UTC"

##########################
# Configuration Settings #
##########################
config: dict
try:
    with open("config.yaml", "r") as config_file:
        config = yaml.full_load(config_file)
except OSError:
    config = {}

COLLOQUIAL_USERNAME = config.get("COLLOQUIAL_USERNAME", "streamer")
TIMEZONE = config.get("TIMEZONE", DEFAULT_TIMEZONE_STR)
