from mrrobot.units import UnitBase

class Unit(UnitBase):
    def __init__(self,config,pipe=None,lock=None):
        super().__init__(config=config,pipe=pipe,lock=lock)
        self.ID         = ("forensics","strings")
        self._RAWMODE   = True
    
    def evaluate(self) -> bool:
        return self._check(self.CODE)