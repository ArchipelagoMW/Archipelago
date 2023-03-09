import typing
from BaseClasses import Location


class KDL3Location(Location):
    game: str = "Kirby's Dream Land 3"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address

