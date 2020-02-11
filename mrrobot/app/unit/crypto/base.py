from app.unit.base import UnitBase

import re
from abc import ABC,abstractmethod

class Crypto(UnitBase,ABC):
    def __init__(self, raw):
        self.raw        = raw
        self.code       = list()
        self.regex      = rb".*"

    def clean(self):
        pattern = re.compile(self.regex)
        self.code = pattern.findall(self.raw)

    def check(self):
        return len(self.code) != 0

    @abstractmethod
    def evaluate(self):
        raise NotImplementedError

    def run(self):
        self.verbose()
        result = None
        self.clean()
        if self.check(): result = self.evaluate()
        return result
