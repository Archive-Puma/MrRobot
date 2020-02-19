from mrrobot.units import UnitBase

class Unit(UnitBase):
    def __init__(self,config,pipe=None,lock=None):
        super().__init__(config=config,pipe=pipe,lock=lock)
        self.ID     = ("crypto","whitespace")
        self._REGEX = rb"([ \t])"
  
    def evaluate(self) -> bool:
        found = False
        bitstring = str()
        for code in self.CODE:
            if code == b'\x20':     bitstring += '0'
            elif code == b'\x09':   bitstring += '1'
        result = int(bitstring,2).to_bytes((len(bitstring) + 7 // 8),byteorder="big")
        result = bytes([ byte for byte in filter(lambda b: b != 0, result) ])
        found = self._check(result)
        return found