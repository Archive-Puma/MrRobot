from units import UnitBase

import base64

class Unit(UnitBase):
    def __init__(self,config,pipe=None,lock=None):
        super().__init__(config=config,pipe=pipe,lock=lock)
        self.ID     = ("crypto","base64")
        self._REGEX = rb"\b([a-zA-Z0-9\+/]+=*)\b"
    
    def evaluate(self) -> bool:
        idx = 0
        found = False
        while not found and idx < len(self.CODE):
            if len(self.CODE[idx]) % 4 == 0:
                decoded = base64.decodebytes(self.CODE[idx])
                found = self._check(decoded)
            idx += 1
        return found