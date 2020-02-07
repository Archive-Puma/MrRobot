from abc import ABC, abstractmethod

class UnitBase(ABC):
    @abstractmethod
    def id(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError

    def verbose(self):
        print(f"-- Running {self.id()}")
        
