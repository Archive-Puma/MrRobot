from app.unit.base import UnitBase

import re
from abc import ABC,abstractmethod

class Esoteric(UnitBase,ABC):
    def __init__(self, raw):
        self.raw        = raw
        self.code       = list()
        self.regex      = ".*"

    def clean(self):
        pattern = re.compile(self.regex)
        self.code = pattern.findall(self.raw)

    def check(self):
        return len(self.code) != 0

    @abstractmethod
    def evaluate(self):
        raise NotImplementedError

    def run(self):
        result = None

        self.clean()
        if self.check(): result = self.evaluate()
        return result
