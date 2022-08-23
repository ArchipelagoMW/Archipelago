from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]


class Overcooked2Item(Item):
    game: str = "Overcooked! 2"


item_table = {
    "Wood"                          : ItemData(1  , True),
    "Coal Bucket"                   : ItemData(2  , True),
    "Spare Plate"                   : ItemData(3  , True),
    "Fire Extinguisher"             : ItemData(4  , True),
    "Bellows"                       : ItemData(5  , True),
    "Clean Dishes"                  : ItemData(6  , True),
    "Progressive Tip Jar"           : ItemData(7  , True),
    "Dash"                          : ItemData(8  , True),
    "Throw"                         : ItemData(9  , True),
    "Catch"                         : ItemData(10 , True),
    "Remote Control Batteries"      : ItemData(11 , True),
    "Wok Wheels"                    : ItemData(12 , True),
    "Dish Scrubber"                 : ItemData(13 , True),
    "Burn Leniency"                 : ItemData(14 , True),
    "Sharp Knife"                   : ItemData(15 , True),
    "Progressive Order Lookahead"   : ItemData(16 , True),
    "Lightweight Backpack"          : ItemData(17 , True),
    "Faster Respawn Time"           : ItemData(18 , True),
    "Faster Condiment/Drink Switch" : ItemData(19 , True),
    "Kevin 1"                       : ItemData(20 , True),
    "Kevin 2"                       : ItemData(21 , True),
    "Kevin 3"                       : ItemData(22 , True),
    "Kevin 4"                       : ItemData(23 , True),
    "Kevin 5"                       : ItemData(24 , True),
    "Kevin 6"                       : ItemData(25 , True),
    "Kevin 7"                       : ItemData(26 , True),
    "Kevin 8"                       : ItemData(27 , True),
    "Ok Emote"                      : ItemData(28 , True),
    "Cooking Emote"                 : ItemData(29 , True),
    "Curse Emote"                   : ItemData(30 , True),
    "Serving Emote"                 : ItemData(31 , True),
    "Preparing Emote"               : ItemData(32 , True),
    "Washing Up Emote"              : ItemData(33 , True),
    "Guest Patience"                : ItemData(34 , True),

    "Victory": ItemData(None, True),
}

item_frequencies = {
    "Progressive Tip Jar": 2,
    "Progressive Order Lookahead": 2,
}

lookup_id_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}
