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
    "Tile 1": AdvData(81000, 'Overworld'),
    "Tile 2": AdvData(81001, 'Overworld'),
    "Tile 3": AdvData(81002, 'Overworld'),
    "Tile 4": AdvData(81003, 'Overworld'),
    "Tile 5": AdvData(81004, 'Overworld'),
    "Tile 6": AdvData(81005, 'Overworld'),
    "Tile 7": AdvData(81006, 'Overworld'),
    "Tile 8": AdvData(81007, 'Overworld'),
    "Tile 9": AdvData(81008, 'Overworld'),
    "Tile 10": AdvData(81009, 'Overworld'),
    "Tile 11": AdvData(81010, 'Overworld'),
    "Tile 12": AdvData(81011, 'Overworld'),
    "Tile 13": AdvData(81012, 'Overworld'),
    "Tile 14": AdvData(81013, 'Overworld'),
    "Tile 15": AdvData(81014, 'Overworld'),
    "Tile 16": AdvData(81015, 'Overworld'),
    "Tile 17": AdvData(81016, 'Overworld'),
    "Tile 18": AdvData(81017, 'Overworld'),
    "Tile 19": AdvData(81018, 'Overworld'),
    "Tile 20": AdvData(81019, 'Overworld'),
    "Tile 21": AdvData(81020, 'Overworld'),
    "Tile 22": AdvData(81021, 'Overworld'),
    "Tile 23": AdvData(81022, 'Overworld'),
    "Tile 24": AdvData(81023, 'Overworld'),
    "Tile 25": AdvData(81024, 'Overworld'),
}

exclusion_table = {
}

events_table = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in advancement_table.items() if data.id}