from units import UnitBase

import base64

class Unit(UnitBase):
    def __init__(self,config,pipe=None,lock=None):
        super().__init__(config=config,pipe=pipe,lock=lock)
        self.ID     = ("crypto","base64")
        self._REGEX = rb"\b([a-zA-Z0-9\+/]+=*)\b"
    
    def evaluate(self) -> bool:
        found = True
        for code in self.CODE:
            if len(code) % 4 == 0:
                decoded = base64.decodebytes(code)
                found = self._check(decoded)
        return found