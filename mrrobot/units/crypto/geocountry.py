from mrrobot.units import UnitBase

import requests

class Unit(UnitBase):
    def __init__(self,config,pipe=None,lock=None):
        super().__init__(config=config,pipe=pipe,lock=lock)
        self.ID     = ("crypto","geocountry")
        self._REGEX = rb"(\-?[0-9\.]+)"

    def _is_valid(self) -> bool:
        return super()._is_valid() and len(self.CODE) % 2 == 0
    
    def evaluate(self) -> bool:
        idx, result = 0, bytes()
        try:
            while idx < len(self.CODE):
                lat = str(self.CODE[idx],encoding=self._CONFIG.ENCODING)
                lon = str(self.CODE[idx+1],encoding=self._CONFIG.ENCODING)
                api = requests.get(f"https://geocode.xyz/{lat},{lon}?json=1")
                json = api.json()
                if "geocode" in json:
                    letter = json["geocode"][0]
                    result += bytes(letter,encoding=self._CONFIG.ENCODING)
                    idx += 2
        except: pass
        return self._check(result)