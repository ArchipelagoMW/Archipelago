import typing

from BaseClasses import Item, ItemClassification
from . import Names

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: int
    event: bool = False

class SADV2Item(Item):
    game: str = "Sonic Advance 2"

    def __init__(self, name, classification: ItemClassification, code: int = None, player: int = None):
        super(SADV2Item, self).__init__(name, classification, code, player)

character_table = {
    Names.sonic_unlock: ItemData(100, 1),
    Names.cream_unlock: ItemData(101, 1),
    Names.tails_unlock: ItemData(102, 1),
    Names.knuckles_unlock: ItemData(103, 1),
    Names.amy_unlock: ItemData(104, 1)
}

zone_table = {
    Names.lf_unlock: ItemData(200, 1),
    Names.hc_unlock: ItemData(201, 1),
    Names.mp_unlock: ItemData(202, 1),
    Names.ip_unlock: ItemData(203, 1),
    Names.sc_unlock: ItemData(204, 1),
    Names.tb_unlock: ItemData(205, 1),
    Names.eu_unlock: ItemData(206, 1),
    Names.xx_unlock: ItemData(207, 2)
}

emerald_table = {
    Names.red_emerald: ItemData(300, 2),
    Names.blue_emerald: ItemData(301, 2),
    Names.yellow_emerald: ItemData(302, 2),
    Names.green_emerald: ItemData(303, 2),
    Names.white_emerald: ItemData(304, 2),
    Names.cyan_emerald: ItemData(305, 2),
    Names.purple_emerald: ItemData(306, 2)
}

filler_table = {
    "Cheat Code to Unlock Shadow": ItemData(400, 0),
    "The Other Half of the Moon": ItemData(401, 0),
    "Land of Darkness": ItemData(402, 0),
    "Computer Room": ItemData(403, 0),
    "Huge Chao Garden": ItemData(404, 0),
    "Scratch and Grounder": ItemData(405, 0),
    "Bocoe and Decoe": ItemData(406, 0),
    "Orbot and Cubot": ItemData(407, 0),
    "Phantom Ruby": ItemData(408, 0),
    "Every Single Drop of All You've Got": ItemData(409, 0),
    "Every Single Bit of All You Have": ItemData(410, 0)
}

event_table = {
    "XX Coordinates 1": ItemData(None, 1, True),
    "XX Coordinates 2": ItemData(None, 1, True),
    "XX Coordinates 3": ItemData(None, 1, True),
    "XX Coordinates 4": ItemData(None, 1, True),
    "XX Coordinates 5": ItemData(None, 1, True),
    "XX Coordinates 6": ItemData(None, 1, True),
    "XX Coordinates 7": ItemData(None, 1, True),
    "Vanilla Rescued": ItemData(None, 1, True)
}

item_table = {
    **character_table,
    **zone_table,
    **emerald_table,
    **filler_table
}