from units import UnitBase

class Unit(UnitBase):
    def __init__(self,config,pipe=None,lock=None):
        super().__init__(config=config,pipe=pipe,lock=lock)
        self.ID     = ("forensics","strings")
        self._REGEX = rb"(.*)"
    
    def evaluate(self) -> bool:
        idx, found = 0, False
        while not found and idx < len(self.CODE):
            found = self._check(self.CODE[idx])
            idx += 1
        return found