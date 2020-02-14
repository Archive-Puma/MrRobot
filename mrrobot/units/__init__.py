import re
from typing import Any
from abc import ABC, abstractmethod
from itertools import chain
from multiprocessing import Lock, Pipe, Process

from app.globals import ENCODING,ENCODING_OPTIONS,FLAG

class UnitBase(ABC):
    def __init__(self, pipe:Pipe=None, lock:Lock=None):
        # Public attributes
        self.ID         = ("Not defined","Not defined")
        self.CODE       = bytes()
        # Protected attributes
        self._RAW       = bytes()
        self._REGEX     = rb"(.*)"
        self._RESULT    = bytes()
        # Multiprocessing
        self._LOCK      = lock
        self._PIPE      = pipe
        self._PRIORITY  = 50 # TODO: Implement priority
    
    # --- Multiprocessing-based methods ---

    def __send(self, response:Any, additional_data:list=None) -> None:
        # Convert the response to a list
        if not response is list: response = [response]
        # Send the response to the parent
        self._PIPE.send((self.ID,response,additional_data))

    def set_priority(self, priority:int) -> object:
        self._PRIORITY = priority
        return self

    # --- Public methods ---
    
    def clean(self, returntype:type=list) -> object:
        # Filter using regular expressions
        regex = re.compile(self._REGEX)
        finds = regex.findall(self._RAW)
        # Convert result to a single list
        result = [*finds]
        # Convert the result in a single bytestring
        if returntype is bytes: result = b"".join(result)
        # Set the result
        self.CODE = result
        # Returns itself to concatenate methods
        return self

    def input(self, inpt) -> object:
        # Check if the encoding is valid
        global ENCODING
        if not ENCODING in ENCODING_OPTIONS: ENCODING = ENCODING_OPTIONS[0]
        # Set the input as a bytestring
        self._RAW = inpt if type(inpt) is bytes else bytes(inpt,encoding=ENCODING)
        # Returns itself to concatenate methods
        return self

    def run(self) -> None:
        try:
            # Evaluate the code if is a valid challenge
            if self._is_valid():
                self.__verbose()
                self.evaluate()
        except KeyboardInterrupt:
            pass

    # --- Protected methods ---

    def _check(self, result:bytes, additional_data:list=None) -> bool:
        found:bool = False
        # Check if a result exists
        if result:
            # Compile the pattern
            pattern:re.Pattern = re.compile(FLAG)
            # Search any flag
            filtered:list = pattern.findall(result)
            # Check if a flag was in
            if len(filtered) > 0:
                found = True
                flag:str = "".join([ str(flag, encoding=ENCODING) for flag in filtered ])
                self.__send(flag, additional_data)
        # Return the result
        return found

    def _is_valid(self) -> bool:
        # Check the length of the code
        return len(self.CODE) > 0

    # --- Private methods ---

    def __verbose(self) -> None:
        # Print some information
        category,unit = self.ID
        print(f"[*] Running {category}: {unit}")

    # --- Abstract methods ---

    @abstractmethod
    def evaluate(self) -> bool:
        raise NotImplementedError