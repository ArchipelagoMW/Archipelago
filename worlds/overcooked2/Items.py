from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]


class Overcooked2Item(Item):
    game: str = "Overcooked! 2"


item_table: dict[str, ItemData] = {
    "Wood"                          : ItemData(0),
    "Coal Bucket"                   : ItemData(1),
    "Spare Plate"                   : ItemData(2),
    "Fire Extinguisher"             : ItemData(3),
    "Bellows"                       : ItemData(4),
    "Clean Dishes"                  : ItemData(5),
    "Progressive Tip Jar"           : ItemData(6),
    "Progressive Tip Jar"           : ItemData(7),
    "Dash"                          : ItemData(8),
    "Throw"                         : ItemData(9),
    "Catch"                         : ItemData(10),
    "Remote Control Batteries"      : ItemData(11),
    "Wok Wheels"                    : ItemData(12),
    "Dish Scrubber"                 : ItemData(13),
    "Burn Leniency"                 : ItemData(14),
    "Sharp Knife"                   : ItemData(15),
    "Progressive Order Lookahead"   : ItemData(16),
    "Progressive Order Lookahead"   : ItemData(17),
    "Lightweight Backpack"          : ItemData(18),
    "Faster Respawn Time"           : ItemData(19),
    "Faster Condiment/Drink Switch" : ItemData(20),
    "Guest Patience"                : ItemData(21),
    "Kevin 1"                       : ItemData(22),
    "Kevin 2"                       : ItemData(23),
    "Kevin 3"                       : ItemData(24),
    "Kevin 4"                       : ItemData(25),
    "Kevin 5"                       : ItemData(26),
    "Kevin 6"                       : ItemData(27),
    "Kevin 7"                       : ItemData(29),
    "Kevin 8"                       : ItemData(29),
    "Ok Emote"                      : ItemData(30),
    "Cooking Emote"                 : ItemData(31),
    "Curse Emote"                   : ItemData(32),
    "Serving Emote"                 : ItemData(33),
    "Preparing Emote"               : ItemData(34),
    "Washing Up Emote"              : ItemData(35),
}

item_id_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}

item_name_to_id: typing.Dict[str, int] = {
    item_name: data.code for item_name, data in item_table.items() if data.code
}

def is_progression(item_name: str) -> bool:
    return "Emote" not in item_name