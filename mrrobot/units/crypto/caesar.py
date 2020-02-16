from units import UnitBase

from string import ascii_lowercase

class Unit(UnitBase):
    def __init__(self,config,pipe=None,lock=None):
        super().__init__(config=config,pipe=pipe,lock=lock)
        self.ID     = ("crypto","caesar")
        self._REGEX = rb"([ -~]+)"
        self.__LOWER = ascii_lowercase
        self.__UPPER = ascii_lowercase.upper()
    
    def evaluate(self) -> bool:
        found = False
        for key in range(len(self.__LOWER)):
            result = self.__caesar(key=key)
            found &= self._check(result, [("Key",key)])
        return found

    def __caesar(self,key:int=13) -> bytes:
        result = str()
        for string in self.CODE:
            for char in string:
                char = chr(char)
                alphabet = None
                # Check alphabets
                if char in self.__LOWER:    alphabet = self.__LOWER
                elif char in self.__UPPER:  alphabet = self.__UPPER
                # Check if is a letter
                if alphabet:
                    idx = alphabet.index(char) - key
                    if idx < 0: idx += len(alphabet)
                    result += alphabet[idx]
                else: result += char
        return bytes(result,encoding=self._CONFIG.ENCODING)