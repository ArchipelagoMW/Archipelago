import typing

from BaseClasses import Item, ItemClassification

from .Names import ItemName


class WL4Item(Item):
    game: str = "Wario Land 4"


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification
    quantity: int = 1

# Items are encoded as 8-bit numbers as follows:
#                   | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
# Jewel pieces:     | 0   0   0 |  passage  | qdrnt |
# CD:               | 0   0   1 |  passage  | level |
#
# Junk items:       | 0   1   0   0 |     type      |
# AP item:          | 1   1   1   1   0   0   0   0 |
#
# For jewel pieces:
#  - passage = 0-5 for entry/emerald/ruby/topaz/sapphire/golden
#  - qdrnt = quadrant, increasing counterclockwise from top left
#
# For CDs:
#  - passage = 0-5 same as jewel pieces, but only 1-4 has a CD
#  - level = increasing as the level goes deeper
#
# Type for junk items:
#  - 0 = Full health item
#  - 1 = Wario form trap
#  - 2 = Single heart recovery
#  - 3 = Single heart damage
#
# For Archipelago, the IDs are the encoded values appended to 0xEC, which is
# Wario Land 4's checksum.

def item_id(encoded_id):
    return 0xEC00 | encoded_id

def jewel_id(passage, quadrant):
    return item_id(passage << 2 | quadrant)

def cd_id(track_no):
    return item_id(1 << 5 | track_no + (1 << 2))

def keyzer_id(level):
    return 1 << 4 | cd_id(level)

box_table = {
    # Entry Passage
    ItemName.entry_passage_jewel.ne: ItemData(jewel_id(0, 0), ItemClassification.progression),
    ItemName.entry_passage_jewel.se: ItemData(jewel_id(0, 1), ItemClassification.progression),
    ItemName.entry_passage_jewel.sw: ItemData(jewel_id(0, 2), ItemClassification.progression),
    ItemName.entry_passage_jewel.nw: ItemData(jewel_id(0, 3), ItemClassification.progression),
    # Emerald Passage
    ItemName.emerald_passage_jewel.ne: ItemData(jewel_id(1, 0), ItemClassification.progression, 4),
    ItemName.emerald_passage_jewel.se: ItemData(jewel_id(1, 1), ItemClassification.progression, 4),
    ItemName.emerald_passage_jewel.sw: ItemData(jewel_id(1, 2), ItemClassification.progression, 4),
    ItemName.emerald_passage_jewel.nw: ItemData(jewel_id(1, 3), ItemClassification.progression, 4),
    ItemName.palm_tree_paradise.cd:    ItemData(cd_id(0), ItemClassification.filler),
    ItemName.wildflower_fields.cd:     ItemData(cd_id(1), ItemClassification.filler),
    ItemName.mystic_lake.cd:           ItemData(cd_id(2), ItemClassification.filler),
    ItemName.monsoon_jungle.cd:        ItemData(cd_id(3), ItemClassification.filler),
    # Ruby Passage
    ItemName.ruby_passage_jewel.ne: ItemData(jewel_id(2, 0), ItemClassification.progression, 4),
    ItemName.ruby_passage_jewel.se: ItemData(jewel_id(2, 1), ItemClassification.progression, 4),
    ItemName.ruby_passage_jewel.sw: ItemData(jewel_id(2, 2), ItemClassification.progression, 4),
    ItemName.ruby_passage_jewel.nw: ItemData(jewel_id(2, 3), ItemClassification.progression, 4),
    ItemName.curious_factory.cd:    ItemData(cd_id(4), ItemClassification.filler),
    ItemName.toxic_landfill.cd:     ItemData(cd_id(5), ItemClassification.filler),
    ItemName.forty_below_fridge.cd: ItemData(cd_id(6), ItemClassification.filler),
    ItemName.pinball_zone.cd:       ItemData(cd_id(7), ItemClassification.filler),
    # Topaz Passage
    ItemName.topaz_passage_jewel.ne: ItemData(jewel_id(3, 0), ItemClassification.progression, 4),
    ItemName.topaz_passage_jewel.se: ItemData(jewel_id(3, 1), ItemClassification.progression, 4),
    ItemName.topaz_passage_jewel.sw: ItemData(jewel_id(3, 2), ItemClassification.progression, 4),
    ItemName.topaz_passage_jewel.nw: ItemData(jewel_id(3, 3), ItemClassification.progression, 4),
    ItemName.toy_block_tower.cd:     ItemData(cd_id(8), ItemClassification.filler),
    ItemName.big_board.cd:           ItemData(cd_id(9), ItemClassification.filler),
    ItemName.doodle_woods.cd:        ItemData(cd_id(10), ItemClassification.filler),
    ItemName.domino_row.cd:          ItemData(cd_id(11), ItemClassification.filler),
    # Sapphire Passage
    ItemName.sapphire_passage_jewel.ne: ItemData(jewel_id(4, 0), ItemClassification.progression, 4),
    ItemName.sapphire_passage_jewel.se: ItemData(jewel_id(4, 1), ItemClassification.progression, 4),
    ItemName.sapphire_passage_jewel.sw: ItemData(jewel_id(4, 2), ItemClassification.progression, 4),
    ItemName.sapphire_passage_jewel.nw: ItemData(jewel_id(4, 3), ItemClassification.progression, 4),
    ItemName.crescent_moon_village.cd:  ItemData(cd_id(12), ItemClassification.filler),
    ItemName.arabian_night.cd:          ItemData(cd_id(13), ItemClassification.filler),
    ItemName.fiery_cavern.cd:           ItemData(cd_id(14), ItemClassification.filler),
    ItemName.hotel_horror.cd:           ItemData(cd_id(15), ItemClassification.filler),
    # Golden Pyramid
    ItemName.golden_pyramid_jewel.ne: ItemData(jewel_id(5, 0), ItemClassification.progression),
    ItemName.golden_pyramid_jewel.se: ItemData(jewel_id(5, 1), ItemClassification.progression),
    ItemName.golden_pyramid_jewel.sw: ItemData(jewel_id(5, 2), ItemClassification.progression),
    ItemName.golden_pyramid_jewel.nw: ItemData(jewel_id(5, 3), ItemClassification.progression),
}

health_table = {
    ItemName.full_health: ItemData(item_id(0x40), ItemClassification.useful),
}

event_table = {
    ItemName.defeated_boss: ItemData(None, ItemClassification.progression),
    ItemName.victory: ItemData(None, ItemClassification.progression),
}

junk_table = {
    ItemName.wario_form: ItemData(item_id(0x41), ItemClassification.trap),
    ItemName.health:     ItemData(item_id(0x42), ItemClassification.filler),
    ItemName.lightning:  ItemData(item_id(0x43), ItemClassification.trap),
}

item_table = {
    **box_table,
    **health_table,
    **event_table,
    **junk_table,
}

lookup_id_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}
