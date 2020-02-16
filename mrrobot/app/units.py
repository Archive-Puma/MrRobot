import pkgutil
from os import path
from pathlib import Path
from importlib import import_module

class UnitLoader:
    def __init__(self):
        self.__UNITS:dict = dict()
        self.__UNITS_FOLDER:Path = \
            path.join(Path(__file__).parent.parent,"units")
        
    def load(self,config) -> dict:
        units:dict = dict()
        for (_,category,_) in pkgutil.iter_modules([self.__UNITS_FOLDER]):
            if config.check_category(category):
                units[category] = self.__load_category(category)
        return units

    def __load_category(self,category:str) -> dict:
        units:dict = dict()
        folder:Path = path.join(self.__UNITS_FOLDER,category)
        for (_,name,_) in pkgutil.iter_modules([folder]):
            # Disable units writing an underscore
            if name[0] != '_':
                unit = import_module(f"units.{category}.{name}")
                if hasattr(unit,"Unit"): units[name] = unit
        return units