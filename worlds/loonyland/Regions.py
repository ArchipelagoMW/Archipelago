from typing import NamedTuple, Dict, List
from BaseClasses import Region
class LoonylandRegion(Region):
    game = "Loonyland"

class LLRegion(NamedTuple):
    real: bool
    map: str = ""
