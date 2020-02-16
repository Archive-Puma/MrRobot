from app.display import colored,info
from app.configuration import Configuration

import re
from abc import ABC, abstractmethod
from multiprocessing import Lock, Pipe, Process

class UnitBase(ABC):
    def __init__(self,config:Configuration,pipe:Pipe=None,lock:Lock=None):
        # Public attributes
        self.ID         = ("Not defined","Not defined")
        self.CODE       = bytes()
        # Protected attributes
        self._RAW       = bytes()
        self._REGEX     = rb"(.*)"
        self._RESULT    = bytes()
        self._CONFIG    = config
        self._RAWMODE   = False
        self._FILENAME  = None
        self._NOPROCESS = False
        # Multiprocessing
        self._LOCK      = lock
        self._PIPE      = pipe
        self._PRIORITY  = 50 # TODO: Implement priority
    
    # --- Multiprocessing-based methods ---

    def __send(self, response, additional_data:list=None) -> None:
        # Convert the response to a list
        if not response is list: response = [response]
        # Send the response to the parent
        self._PIPE.send((self.ID,response,additional_data))

    def set_priority(self, priority:int) -> object:
        self._PRIORITY = priority
        return self

    # --- Public methods ---
    
    def clean(self, returntype:type=list) -> object:
        if not self._NOPROCESS:
            if self._RAWMODE: self.CODE = self._RAW
            else:
                challenge = self.__inside_challenge(self._RAW) if self._CONFIG.INSIDE else self._RAW
                # Filter using regular expressions
                regex = re.compile(self._REGEX)
                finds = regex.findall(challenge)
                # Convert result to a single list
                result = [*finds]
                # Convert the result in a single bytestring
                if returntype is bytes: result = b"".join(result)
                # Set the result
                self.CODE = result
        # Returns itself to concatenate methods
        return self

    def input(self, challenge:tuple) -> object:
        # Save the input
        self._FILENAME, self._RAW = challenge
        # Returns itself to concatenate methods
        return self

    def run(self) -> None:
        try:
            # Evaluate the code if is a valid challenge
            if self._is_valid():
                self.__verbose("Running",decorator='+')
                self.evaluate()
        except KeyboardInterrupt:
            pass

    # --- Protected methods ---

    def _check(self,result:bytes,additional_data:list=None) -> bool:
        found:bool = False
        # Check if a result exists
        if result:
            if self._CONFIG.INSIDE:
                prefix = bytes(self._CONFIG.FLAG.split('{',1)[0],encoding=self._CONFIG.ENCODING)
                result = prefix + b'{' + result + b'}'                
            # Compile the pattern
            pattern:re.Pattern = re.compile(bytes(self._CONFIG.FLAG,encoding=self._CONFIG.ENCODING))
            # Search any flag
            filtered:list = pattern.findall(result)
            # Check if a flag was in
            if len(filtered) > 0:
                found = True
                flag:str = "".join([ str(flag, encoding=self._CONFIG.ENCODING) for flag in filtered ])
                self.__send(flag, additional_data)
        # Return the result
        return found

    def _is_valid(self) -> bool:
        self.__verbose("Checking")
        # Check the length of the code
        return len(self.CODE) > 0 or (self._NOPROCESS and self._FILENAME)

    # --- Private methods ---

    def __inside_challenge(self,raw:bytes) -> bytes:
        flagformat = bytes(self._CONFIG.FLAG,encoding=self._CONFIG.ENCODING)
        pattern = re.compile(flagformat)
        flags = pattern.findall(raw)
        inside = re.compile(rb"{.*?}")
        challenges = inside.findall(b"\n".join(flags))
        return b"\n".join([ challenge[1:-1] for challenge in challenges ])

    def __verbose(self, action:str, decorator:str="?") -> None:
        # Print some information
        category,unit = self.ID
        info(f"{action} {colored('good')}{category}{colored()} {unit}",decorator=decorator)

    # --- Abstract methods ---

    @abstractmethod
    def evaluate(self) -> bool:
        raise NotImplementedError