from os.path import isfile
from configparser import ConfigParser

# Default configuration
DEFAULT_FILE = "mrrobot.ini"
DEFAULT_FLAG = ".*"
DEFAULT_THREADS = 4

def default():
    # Check if the file exists
    if not isfile(DEFAULT_FILE):
        # Create the configurator
        config = ConfigParser()
        # Set the default values
        config["DEFAULT"] = { "Threads": DEFAULT_THREADS }
        # Set the CTF values
        config["CTF"] = { "Flag": DEFAULT_FLAG }
        # Create the config file
        with open(DEFAULT_FILE, "w") as configfile:
            config.write(configfile)
    # Return the filename
    return DEFAULT_FILE

def configure(config):
    configuration = dict()
    # Default configuration
    if config["DEFAULT"]:
        configuration["Threads"] = config["DEFAULT"]["Threads"] if config["DEFAULT"]["Threads"] else None
    else:
        configuration["Threads"] = None
    # CTF configuration
    if config["CTF"]:
        configuration["Flag"] = config["CTF"]["Flag"] if config["CTF"]["Flag"] else DEFAULT_FLAG
    else:
        configuration["Flag"] = DEFAULT_FLAG
    # Return configuration
    return configuration

def parse(configfile):
    # Read the configuration file
    config = ConfigParser()
    config.read(configfile)
    # Return the parsed configuration
    return configure(config)

