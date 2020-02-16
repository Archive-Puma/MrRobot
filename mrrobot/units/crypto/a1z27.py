from mrrobot.units import UnitBase

class Unit(UnitBase):
    def __init__(self,config,pipe=None,lock=None):
        super().__init__(config=config,pipe=pipe,lock=lock)
        self.ID     = ("crypto","a1z27")
        self._REGEX = rb"(2[0-7]|1[0-9]|0?[1-9]|[_\{\}])"
    
    def evaluate(self) -> bool:
        result = list()
        for token in self.CODE:
            letter = str()
            token = str(token, encoding=self._CONFIG.ENCODING)
            if token.isnumeric():
                token = int(token)
                if token < 15: letter = chr(token + 64)
                elif token == 15: letter = "Ñ"
                else: letter = chr(token + 63)
            else: letter = token
            result.append(letter)
        result = bytes("".join(result), encoding=self._CONFIG.ENCODING)
        return self._check(result)