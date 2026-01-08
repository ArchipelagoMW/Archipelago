import typing

from BaseClasses import Location
from .Puzzle import LARGEST_CUBE

class LocData(typing.NamedTuple):
    id: int
    reqs: dict


class TwistyCubeLocation(Location):
    game: str = "Twisty Cube"

    def __init__(self, player: int, name: str, address: typing.Optional[int], reqs, parent):
        super().__init__(player, name, address, parent)
        self.reqs = reqs
        
location_table = {location: LocData(267780000 + index, index) for location, index in LARGEST_CUBE.get_location_table(1).items()}
