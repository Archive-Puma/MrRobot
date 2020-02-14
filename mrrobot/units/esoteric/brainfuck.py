from units import UnitBase

import re
import sys

class Unit(UnitBase):
    def __init__(self,pipe=None,lock=None):
        super().__init__(pipe=pipe,lock=lock)
        self.ID     = ("esoteric","brainfuck")
        self._REGEX = rb"([><+-.,[\]])"
    
    def evaluate(self) -> bool:
        result,additional_data = self.__brainfuck()
        return self._check(result,additional_data)

    def __brainfuck(self) -> bytes:
        # Variables
        result:list  = list()
        loops:list   = list()
        stack, ip, sp = [0], 0, 0

        # Execution
        while ip < len(self.CODE):
            # Get the current token
            token:bytes = self.CODE[ip]
            # Interpret the token
            if token == b'>':
                sp += 1
                if sp == len(stack): stack.append(0)
            elif token == b'<':
                sp = 0 if sp <= 0 else sp - 1
            elif token == b'+':
                stack[sp] = 0 if stack[sp] == 255 else stack[sp] + 1
            elif token == b'-':
                stack[sp] = 255 if stack[sp] == 0 else stack[sp] - 1
            elif token == b'.':
                result.append(stack[sp])
            elif token == b',':
                key = ord(sys.stdin.read(1))
                stack[sp] = key if key >= 0 and key <= 255 else 0
            elif token == b'[': loops.append(ip)
            elif token == b']':
                if stack[sp] == 0 and len(loops) > 0: loops.pop()
                else: ip = loops[-1]
            # Increment the instruction pointer
            ip += 1

        # Return the result as a bytes-string
        return (bytes(result) if len(result) > 0 else None, [("Accumulator", sp)])