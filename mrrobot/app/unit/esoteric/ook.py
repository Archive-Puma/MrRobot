from app.unit.esoteric.base import Esoteric
from app.unit.esoteric.brainfuck import Unit as Brainfuck

import re

class Unit(Esoteric):
    def __init__(self, raw):
        super().__init__(raw)
        self.regex  = rb"Ook([!?.])"

    def evaluate(self):
        print("---- Ook")
        result = None
        if len(self.code) % 2 == 0:
            bf_code = self.__ook2bf()
            brainfuck = Brainfuck(bf_code)
            result = brainfuck.run()
        return result

    def __ook2bf(self):
        idx = 0
        bf_code = list()
        while idx < len(self.code):
            instruction = self.code[idx] + self.code[idx+1]
            if instruction == b".?":    bf_code.append(b">")
            elif instruction == b"?.":  bf_code.append(b"<")
            elif instruction == b"..":  bf_code.append(b"+")
            elif instruction == b"!!":  bf_code.append(b"-")
            elif instruction == b"!.":  bf_code.append(b".")
            elif instruction == b".!":  bf_code.append(b",")            
            elif instruction == b"!?":  bf_code.append(b"[")
            elif instruction == b"?!":  bf_code.append(b"]")

            idx += 2
        return b"".join(bf_code)