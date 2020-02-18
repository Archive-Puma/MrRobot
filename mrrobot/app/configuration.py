from mrrobot.app.exception import Elliot

from os.path import isfile
from configparser import ConfigParser,ParsingError

class Configuration:
    def __init__(self):
        # Private attributes
        self.__FILE:str = "mrrobot.ini"
        self.__CONFIG:ConfigParser = ConfigParser()
        self.__AVAILABLE_UNITS:list = [
            "crypto","esoteric","forensics"]
        self.__VALID_ENCODINGS:list = [
            "utf-8","utf8","utf_8","UTF","U8"]
        # Public attributes
        self.ENABLED_UNITS  :list   = [ True for _ in self.__AVAILABLE_UNITS ]
        self.ENCODING       :str    = self.__VALID_ENCODINGS[0]
        self.FINDALL        :bool   = False
        self.FLAG           :str    = "MrRobotCTF{.*?}"
        self.INSIDE         :bool   = False
        self.ONLYENABLED    :str    = None
        self.SAFE           :bool   = False
        self.TIMEOUT        :float  = 10.0
        
    # ---x--- Public methods ---x---

    def load(self,configfile:str=None,clean:bool=False) -> None:
        # Check argument
        if not configfile: configfile = self.__FILE
        # Create a default configuration file if needed
        if not isfile(self.__FILE) or clean: self.__create_default()
        # Read the configuration file
        self.__read(configfile)
        # Load the performance parameters
        if self.__CONFIG["PERFORMANCE"]:
            performance = self.__CONFIG["PERFORMANCE"]
            if performance["encoding"]: self.set_encoding(performance["encoding"])
            if performance["timeout"]: self.set_timeout(float(performance["timeout"]))
        # Load the challenge parameters
        if self.__CONFIG["CHALLENGE"]:
            challenge = self.__CONFIG["CHALLENGE"]
            if challenge["findall"]: self.set_findall(challenge["findall"])
            if challenge["flag"]: self.set_flag(challenge["flag"])
            if challenge["units"] and type(challenge["units"]) is list:
                for unit in challenge["units"]: self.enable_category(unit)
                
    # --- Setters
    
    def check_category(self,name:str) -> None:
        idx = self.__AVAILABLE_UNITS.index(name)
        return idx != -1 and self.ENABLED_UNITS[idx]

    def enable_category(self,name:str) -> None:
        idx = self.__AVAILABLE_UNITS.index(name)
        if idx != -1: self.ENABLED_UNITS[idx] = True
    
    def enable_only(self,name:str) -> None:
        self.ONLYENABLED = name

    def set_all_categories(self,enabled:bool=False) -> None:
        self.ENABLED_UNITS:list = [ enabled for _ in self.__AVAILABLE_UNITS ]

    def set_encoding(self,encoding:str=None) -> None:
        if encoding:
            if encoding in self.__VALID_ENCODINGS: self.ENCODING = encoding
            else: raise Elliot(f"Encoding '{encoding}' is not supported")

    def set_findall(self,findall:bool=False) -> None:
        self.FINDALL = findall

    def set_flag(self,flag:str=None) -> None:
        if flag: self.FLAG = flag

    def set_inside(self,inside:bool=False) -> None:
        if inside: self.INSIDE = inside

    def set_safe(self,safe:bool=False) -> None:
        self.SAFE = safe

    def set_timeout(self,timeout:float=None) -> None:
        if timeout: self.TIMEOUT = timeout

    # ---x--- Private methods ---x---

    def __create_default(self) -> None:
        # Set the default values
        self.__CONFIG["PERFORMANCE"] = {
            "encoding": self.ENCODING,
            "timeout":  self.TIMEOUT
        }
        self.__CONFIG["CHALLENGE"] = {
            "findall":  self.FINDALL,
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
        # Check some parameters
        self.set_encoding(self.__CONFIG["PERFORMANCE"]["encoding"])