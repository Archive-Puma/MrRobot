from units import UnitBase

from PIL import Image

class Unit(UnitBase):
    def __init__(self,config,pipe=None,lock=None):
        super().__init__(config=config,pipe=pipe,lock=lock)
        self.ID         = ("forensics","lsb")
        self._NOPROCESS = True

    def _is_valid(self):
        try:
            image = Image.open(self._FILENAME, "r")
            self.CODE = list(image.getdata())
        except: pass
        return super()._is_valid()
        
    def evaluate(self) -> bool:   
        result = self.__steganography()
        return self._check(result)

    def __steganography(self) -> bytes:
        bits = [ rgba[i] % 2 for rgba in self.CODE for i in range(3) ]
        decoded = [ int("".join(map(str,bits[i:i+8])),2) for i in range(0,len(bits),8) ]
        result = bytes(filter(lambda byte: byte != 0, decoded))
        return result