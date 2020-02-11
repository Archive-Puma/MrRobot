from abc import ABC, abstractmethod

class UnitBase(ABC):
    @abstractmethod
    def id(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError

    def verbose(self):
        category, unit = self.id().split("::", 1)
        print(f"[*] Testing {unit} unit from {category} category")

    def priority(self):
        return 50
        
