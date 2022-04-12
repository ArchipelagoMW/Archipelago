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
    "Tile 1": AdvData(81000, 'Board'),
    "Tile 2": AdvData(81001, 'Board'),
    "Tile 3": AdvData(81002, 'Board'),
    "Tile 4": AdvData(81003, 'Board'),
    "Tile 5": AdvData(81004, 'Board'),
    "Tile 6": AdvData(81005, 'Board'),
    "Tile 7": AdvData(81006, 'Board'),
    "Tile 8": AdvData(81007, 'Board'),
    "Tile 9": AdvData(81008, 'Board'),
    "Tile 10": AdvData(81009, 'Board'),
    "Tile 11": AdvData(81010, 'Board'),
    "Tile 12": AdvData(81011, 'Board'),
    "Tile 13": AdvData(81012, 'Board'),
    "Tile 14": AdvData(81013, 'Board'),
    "Tile 15": AdvData(81014, 'Board'),
    "Tile 16": AdvData(81015, 'Board'),
    "Tile 17": AdvData(81016, 'Board'),
    "Tile 18": AdvData(81017, 'Board'),
    "Tile 19": AdvData(81018, 'Board'),
    "Tile 20": AdvData(81019, 'Board'),
    "Tile 21": AdvData(81020, 'Board'),
    "Tile 22": AdvData(81021, 'Board'),
    "Tile 23": AdvData(81022, 'Board'),
    "Tile 24": AdvData(81023, 'Board'),
    "Tile 25": AdvData(81024, 'Board'),
}

exclusion_table = {
}

events_table = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in advancement_table.items() if data.id}