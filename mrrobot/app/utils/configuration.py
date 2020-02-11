from os import cpu_count
from os.path import isfile
from configparser import ConfigParser

# Default configuration
DEFAULT_CODING  = "utf-8"
DEFAULT_FILE    = "mrrobot.ini"
DEFAULT_FLAG    = "MrRobotCTF{.*}"
DEFAULT_THREADS = cpu_count()
DEFAULT_TIMEOUT = 10
DEFAULT_UNITS   = ["crypto","esoteric"]
# Enabled units
UNITS_CATEGORIES    = DEFAULT_UNITS
ALL_UNITS_DISABLED  = [False] * len(DEFAULT_UNITS)

def default():
    # Check if the file exists
    if not isfile(DEFAULT_FILE):
        # Create the configurator
        config = ConfigParser()
        # Set the default values
        config["DEFAULT"] = {
            "Threads": DEFAULT_THREADS, "Timeout": DEFAULT_TIMEOUT, "Coding": DEFAULT_CODING }
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
        configuration["Coding"]     = config["DEFAULT"]["Coding"] if config["DEFAULT"]["Coding"] else DEFAULT_CODING
        configuration["Threads"]    = config["DEFAULT"]["Threads"] if config["DEFAULT"]["Threads"] else DEFAULT_THREADS
        configuration["Timeout"]    = config["DEFAULT"]["Timeout"] if config["DEFAULT"]["Timeout"] else DEFAULT_TIMEOUT
    else:
        configuration["Coding"]     = DEFAULT_CODING
        configuration["Threads"]    = DEFAULT_THREADS
        configuration["Timeout"]    = DEFAULT_TIMEOUT
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

