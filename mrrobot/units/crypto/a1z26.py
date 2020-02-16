from mrrobot.units import UnitBase

class Unit(UnitBase):
    def __init__(self,config,pipe=None,lock=None):
        super().__init__(config=config,pipe=pipe,lock=lock)
        self.ID     = ("crypto","a1z26")
        self._REGEX = rb"(2[0-6]|1[0-9]|0?[1-9]|[_\{\}])"
    
    def evaluate(self) -> bool:
        result = list()
        for token in self.CODE:
            token = str(token, encoding=self._CONFIG.ENCODING)
            letter = chr(int(token) + 64) if token.isnumeric() else token
            result.append(letter)
        result = bytes("".join(result), encoding=self._CONFIG.ENCODING)
        return self._check(result)