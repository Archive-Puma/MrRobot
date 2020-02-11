from app.unit.crypto.base import Crypto

import base64

class Unit(Crypto):
    def __init__(self, raw):
        super().__init__(raw)
        self.regex  = rb"\b([a-zA-Z0-9\+/]+)=*\b"

    def id(self):
        return "crypto::base64"
    
    def evaluate(self):
        return self.__decode()
            
    def __decode(self):
        result  = list()
        decoded = bytes()
        for msg in self.code:
            if len(msg) % 4 == 0:
                decoded = base64.decodebytes(msg)
                result.append(decoded)
        return result
    

