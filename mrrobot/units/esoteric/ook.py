from units import UnitBase
from units.esoteric.brainfuck import Unit as Brainfuck

import sys

class Unit(UnitBase):
    def __init__(self,pipe=None,lock=None):
        super().__init__(pipe=pipe,lock=lock)
        self.ID     = ("esoteric","ook")
        self._REGEX = rb"Ook([!?.])"

    def _is_valid(self) -> bool:
        # Check Ook's parity length
        length:int = len(self.CODE)
        return length > 0 and length % 2 == 0

    def evaluate(self) -> bool:
        bf_code:bytes = self.__ook2bf()
        brainfuck:Brainfuck = Brainfuck(self._PIPE,self._LOCK)
        brainfuck.ID = self.ID
        brainfuck.CODE = bf_code
        return brainfuck.evaluate()

    def __ook2bf(self) -> bytes:
        idx:int = 0
        bf_code:list = list()
        while idx < len(self.CODE):
            instruction = self.CODE[idx] + self.CODE[idx+1]
            if instruction == b".?":    bf_code.append(b">")
            elif instruction == b"?.":  bf_code.append(b"<")
            elif instruction == b"..":  bf_code.append(b"+")
            elif instruction == b"!!":  bf_code.append(b"-")
            elif instruction == b"!.":  bf_code.append(b".")
            elif instruction == b".!":  bf_code.append(b",")            
            elif instruction == b"!?":  bf_code.append(b"[")
            elif instruction == b"?!":  bf_code.append(b"]")

            idx += 2
        return bf_code