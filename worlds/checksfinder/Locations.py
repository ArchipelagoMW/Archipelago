from BaseClasses import Location
import typing


class AdvData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str


class ChecksFinderAdvancement(Location):
    game: str = "ChecksFinder"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address


advancement_table = {
    "Tile 1": AdvData(80000, 'Overworld'),
    "Tile 2": AdvData(80001, 'Overworld'),
    "Tile 3": AdvData(80002, 'Overworld'),
    "Tile 4": AdvData(80003, 'Overworld'),
    "Tile 5": AdvData(80004, 'Overworld'),
    "Tile 6": AdvData(80005, 'Overworld'),
    "Tile 7": AdvData(80006, 'Overworld'),
    "Tile 8": AdvData(80007, 'Overworld'),
    "Tile 9": AdvData(80008, 'Overworld'),
    "Tile 10": AdvData(80009, 'Overworld'),
    "Tile 11": AdvData(80010, 'Overworld'),
    "Tile 12": AdvData(80011, 'Overworld'),
    "Tile 13": AdvData(80012, 'Overworld'),
    "Tile 14": AdvData(80013, 'Overworld'),
    "Tile 15": AdvData(80014, 'Overworld'),
    "Tile 16": AdvData(80015, 'Overworld'),
    "Tile 17": AdvData(80016, 'Overworld'),
    "Tile 18": AdvData(80017, 'Overworld'),
    "Tile 19": AdvData(80018, 'Overworld'),
    "Tile 20": AdvData(80019, 'Overworld'),
    "Tile 21": AdvData(80020, 'Overworld'),
    "Tile 22": AdvData(80021, 'Overworld'),
    "Tile 23": AdvData(80022, 'Overworld'),
    "Tile 24": AdvData(80023, 'Overworld'),
    "Tile 25": AdvData(80024, 'Overworld'),
}

exclusion_table = {
}

events_table = {
}