from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]


class Overcooked2Item(Item):
    game: str = "Overcooked! 2"


item_table = {
    "Wood"                          : ItemData(0   , True),
    "Coal Bucket"                   : ItemData(1   , True),
    "Spare Plate"                   : ItemData(2   , True),
    "Fire Extinguisher"             : ItemData(3   , True),
    "Bellows"                       : ItemData(4   , True),
    "Clean Dishes"                  : ItemData(5   , True),
    "Progressive Tip Jar"           : ItemData(6   , True),
    "Progressive Tip Jar"           : ItemData(7   , True),
    "Dash"                          : ItemData(8   , True),
    "Throw"                         : ItemData(9   , True),
    "Catch"                         : ItemData(10  , True),
    "Remote Control Batteries"      : ItemData(11  , True),
    "Wok Wheels"                    : ItemData(12  , True),
    "Dish Scrubber"                 : ItemData(13  , True),
    "Burn Leniency"                 : ItemData(14  , True),
    "Sharp Knife"                   : ItemData(15  , True),
    "Progressive Order Lookahead"   : ItemData(16  , True),
    "Progressive Order Lookahead"   : ItemData(17  , True),
    "Lightweight Backpack"          : ItemData(18  , True),
    "Faster Respawn Time"           : ItemData(19  , True),
    "Faster Condiment/Drink Switch" : ItemData(20  , True),
    "Guest Patience"                : ItemData(21  , True),
    "Kevin 1"                       : ItemData(22  , True),
    "Kevin 2"                       : ItemData(23  , True),
    "Kevin 3"                       : ItemData(24  , True),
    "Kevin 4"                       : ItemData(25  , True),
    "Kevin 5"                       : ItemData(26  , True),
    "Kevin 6"                       : ItemData(27  , True),
    "Kevin 7"                       : ItemData(29  , True),
    "Kevin 8"                       : ItemData(29  , True),
    "Ok Emote"                      : ItemData(30  , True),
    "Cooking Emote"                 : ItemData(31  , True),
    "Curse Emote"                   : ItemData(32  , True),
    "Serving Emote"                 : ItemData(33  , True),
    "Preparing Emote"               : ItemData(34  , True),
    "Washing Up Emote"              : ItemData(35  , True),
    "Victory"                       : ItemData(None, True),
}

pickup_id_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}

def is_progression(item_name: str) -> bool:
    return "Emote" not in item_name