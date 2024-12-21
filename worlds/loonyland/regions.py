from typing import NamedTuple

from BaseClasses import Region


class LoonylandRegion(Region):
    game = "Loonyland"

class LLRegion(NamedTuple):
    real: bool
    map: str = ""
