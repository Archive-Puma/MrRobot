from os import cpu_count
from os.path import isfile
from configparser import ConfigParser

# Default configuration
DEFAULT_FILE    = "mrrobot.ini"
DEFAULT_FLAG    = ".*"
DEFAULT_THREADS = cpu_count()
DEFAULT_TIMEOUT = 10
DEFAULT_UNITS   = ["esoteric"]
# Enabled units
ALL_UNITS_DISABLED = [False]
UNITS_CATEGORIES = ["esoteric"]

def default():
    # Check if the file exists
    if not isfile(DEFAULT_FILE):
        # Create the configurator
        config = ConfigParser()
        # Set the default values
        config["DEFAULT"] = { "Threads": DEFAULT_THREADS, "Timeout": DEFAULT_TIMEOUT }
        # Set the CTF values
        config["CTF"] = { "Flag": DEFAULT_FLAG, "Units": DEFAULT_UNITS }
        # Create the config file
        with open(DEFAULT_FILE, "w") as configfile:
            config.write(configfile)
    # Return the filename
    return DEFAULT_FILE

def configure(config):
    configuration = dict()
    # Default configuration
    if config["DEFAULT"]:
        configuration["Threads"] = config["DEFAULT"]["Threads"] if config["DEFAULT"]["Threads"] else DEFAULT_THREADS
        configuration["Timeout"] = config["DEFAULT"]["Timeout"] if config["DEFAULT"]["Timeout"] else DEFAULT_TIMEOUT
    else:
        configuration["Threads"] = DEFAULT_THREADS
        configuration["Timeout"] = DEFAULT_TIMEOUT
    # CTF configuration
    configuration["Units"] = ALL_UNITS_DISABLED
    if config["CTF"]:
        configuration["Flag"]   = config["CTF"]["Flag"] if config["CTF"]["Flag"] else DEFAULT_FLAG
        # Enable the units
        units = config["CTF"]["Units"] if config["CTF"]["Units"] and type(config["CTF"]["Units"]) is list else DEFAULT_UNITS
        for unit in units:
            if unit in UNITS_CATEGORIES:
                idx = UNITS_CATEGORIES.index(unit)
                configuration["Units"][idx] = True
    else:
        configuration["Flag"]   = DEFAULT_FLAG
        configuration["Units"]  = ALL_UNITS_DISABLED
    # Return configuration
    return configuration

def parse(configfile):
    # Read the configuration file
    config = ConfigParser()
    config.read(configfile)
    # Return the parsed configuration
    return configure(config)

