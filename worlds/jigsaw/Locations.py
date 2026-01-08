import typing

from BaseClasses import Location

class LocData(typing.NamedTuple):
    id: int
    region: str


class JigsawLocation(Location):
    game: str = "Jigsaw"

    def __init__(self, player: int, name: str, address: typing.Optional[int], nmerges: int, parent):
        super().__init__(player, name, address, parent)
        self.nmerges = nmerges

location_table = {f"Merge {i} times": LocData(234782000 + i, "Board") for i in range(1, 2501)}