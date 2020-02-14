from app.exception import Elliot

from os.path import isfile
from configparser import ConfigParser,ParsingError

class Configuration:
    def __init__(self):
        # Public attributes
        self.CODING     :str    = "utf-8"
        self.FLAG       :bytes  = rb"(.*)"
        self.TIMEOUT    :float  = 10.0
        # Private attributes
        self.__FILE:str = "mrrobot.ini"
        self.__CONFIG:ConfigParser = ConfigParser()
        self.__AVAILABLE_UNITS:list = [
            "crypto","esoteric"]

    def load(self,configfile:str=None,clean:bool=False) -> None:
        # Check argument
        if not configfile: configfile = self.__FILE
        # Create a default configuration file if needed
        if not isfile(self.__FILE) or clean: self.__create_default()
        # Read the configuration file
        self.__read(configfile)

    def __create_default(self) -> None:
        # Set the default values
        self.__CONFIG["PERFORMANCE"] = {
            "coding":   self.CODING,
            "timeout":  self.TIMEOUT
        }
        self.__CONFIG["CHALLENGE"] = {
            "flag":     self.FLAG,
            "units":    self.__AVAILABLE_UNITS
        }
        # Create the config file
        with open(self.__FILE, "w") as configfile:
            self.__CONFIG.write(configfile)

    def __read(self,configfile:str) -> None:
        # Check if file exists
        if not isfile(configfile):
            raise Elliot(f"{configfile} is not a file")
        # Read the configuration
        try: self.__CONFIG.read(configfile)
        except ParsingError:
            raise Elliot(f"{configfile} is not a valid configuration file")

