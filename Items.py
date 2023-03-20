import typing

from BaseClasses import Item

from .Names import ItemName


class WL4Item(Item):
    game: str = "Wario Land 4"


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    quantity: int = 1

# Items are encoded as 8-bit numbers as follows:
#                   | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
# Jewel pieces:     | 0   0   0 |  passage  | qdrnt |
# CD:               | 0   1   0 |  passage  | level |
#
# Full health item: | 1   0   0   0   0   0   0   0 |
# Wario form trap:  | 1   0   0   1   0   0   0   0 |
# Heart/Lightning:  | 1   0   1   0   0   0   0 | ? |
# Coin:             | 1   0   1   1 |  denomination |
#
# For jewel pieces:
#  - passage = 0-5 for entry/emerald/ruby/topaz/sapphire/golden
#  - qdrnt = quadrant, increasing counterclockwise from top left
#
# For CDs:
#  - passage = 0-5 same as jewel pieces, but only 1-4 has a CD
#  - level = increasing as the level goes deeper
#
# For junk items:
#  - The full health item is unique (as in, all are identical)
#  - Same with Wario form traps (which form you get is random)
#  - Heart/lightning: ? is 0 if heart, 1 if lightning
#
# For Archipelago, the IDs are the encoded values appended to 0xEC, which is
# Wario Land 4's checksum.

def item_id(encoded_id):
    return 0xEC00 | encoded_id

def jewel_id(passage, quadrant):
    return item_id(passage << 2 | quadrant)

def cd_id(track_no):
    return item_id(1 << 6 | track_no + (1 << 2))

def keyzer_id(level):
    return 1 << 4 | cd_id(level)

box_table = {
    # Entry Passage
    ItemName.entry_passage_jewel.ne: ItemData(jewel_id(0, 0), True),
    ItemName.entry_passage_jewel.se: ItemData(jewel_id(0, 1), True),
    ItemName.entry_passage_jewel.sw: ItemData(jewel_id(0, 2), True),
    ItemName.entry_passage_jewel.nw: ItemData(jewel_id(0, 3), True),
    # Emerald Passage
    ItemName.emerald_passage_jewel.ne: ItemData(jewel_id(1, 0), True, 4),
    ItemName.emerald_passage_jewel.se: ItemData(jewel_id(1, 1), True, 4),
    ItemName.emerald_passage_jewel.sw: ItemData(jewel_id(1, 2), True, 4),
    ItemName.emerald_passage_jewel.nw: ItemData(jewel_id(1, 3), True, 4),
    ItemName.palm_tree_paradise.cd:    ItemData(cd_id(0), False),
    ItemName.wildflower_fields.cd:     ItemData(cd_id(1), False),
    ItemName.mystic_lake.cd:           ItemData(cd_id(2), False),
    ItemName.monsoon_jungle.cd:        ItemData(cd_id(3), False),
    # Ruby Passage
    ItemName.ruby_passage_jewel.ne: ItemData(jewel_id(2, 0), True, 4),
    ItemName.ruby_passage_jewel.se: ItemData(jewel_id(2, 1), True, 4),
    ItemName.ruby_passage_jewel.sw: ItemData(jewel_id(2, 2), True, 4),
    ItemName.ruby_passage_jewel.nw: ItemData(jewel_id(2, 3), True, 4),
    ItemName.curious_factory.cd:    ItemData(cd_id(4), False),
    ItemName.toxic_landfill.cd:     ItemData(cd_id(5), False),
    ItemName.forty_below_fridge.cd: ItemData(cd_id(6), False),
    ItemName.pinball_zone.cd:       ItemData(cd_id(7), False),
    # Topaz Passage
    ItemName.topaz_passage_jewel.ne: ItemData(jewel_id(3, 0), True, 4),
    ItemName.topaz_passage_jewel.se: ItemData(jewel_id(3, 1), True, 4),
    ItemName.topaz_passage_jewel.sw: ItemData(jewel_id(3, 2), True, 4),
    ItemName.topaz_passage_jewel.nw: ItemData(jewel_id(3, 3), True, 4),
    ItemName.toy_block_tower.cd:     ItemData(cd_id(8), False),
    ItemName.big_board.cd:           ItemData(cd_id(9), False),
    ItemName.doodle_woods.cd:        ItemData(cd_id(10), False),
    ItemName.domino_row.cd:          ItemData(cd_id(11), False),
    # Sapphire Passage
    ItemName.sapphire_passage_jewel.ne: ItemData(jewel_id(4, 0), True, 4),
    ItemName.sapphire_passage_jewel.se: ItemData(jewel_id(4, 1), True, 4),
    ItemName.sapphire_passage_jewel.sw: ItemData(jewel_id(4, 2), True, 4),
    ItemName.sapphire_passage_jewel.nw: ItemData(jewel_id(4, 3), True, 4),
    ItemName.crescent_moon_village.cd:  ItemData(cd_id(12), False),
    ItemName.arabian_night.cd:          ItemData(cd_id(13), False),
    ItemName.fiery_cavern.cd:           ItemData(cd_id(14), False),
    ItemName.hotel_horror.cd:           ItemData(cd_id(15), False),
    # Golden Pyramid
    ItemName.golden_pyramid_jewel.ne: ItemData(jewel_id(5, 0), True),
    ItemName.golden_pyramid_jewel.se: ItemData(jewel_id(5, 1), True),
    ItemName.golden_pyramid_jewel.sw: ItemData(jewel_id(5, 2), True),
    ItemName.golden_pyramid_jewel.nw: ItemData(jewel_id(5, 3), True),
    # Full Health Item
    ItemName.full_health: ItemData(item_id(0x80), False, 17),
}

event_table = {
    ItemName.defeated_boss: ItemData(None, True),
    ItemName.victory: ItemData(None, True),
}

junk_table = {
    ItemName.wario_form: ItemData(item_id(0x90), False),
    ItemName.health:     ItemData(item_id(0xA0), False),
    ItemName.lightning:  ItemData(item_id(0xA1), False),
}

item_table = {
    **box_table,
    **event_table,
    **junk_table,
}

lookup_id_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}
