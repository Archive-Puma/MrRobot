from app.unit.esoteric.base import Esoteric

import re
import sys

class Unit(Esoteric):
    def __init__(self, raw):
        super().__init__(raw)
        self.regex  = rb"[><+-.,[\]]"

    def evaluate(self):
        print("---- Brainfuck")
        return self.__brainfuck()
            
    def __brainfuck(self):
        result  = list()
        loops   = list()
        stack, ip, sp = [0], 0, 0

        while ip < len(self.code):
            token = self.code[ip]

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
            elif token == b'[':
                loops.append(ip)
            elif token == b']':
                if stack[sp] == 0 and len(loops) > 0:
                    loops.pop()
                else:
                    ip = loops[-1]
            ip += 1
        return "".join(map(chr,result))

    

