import typing

from BaseClasses import Item

from .Names import ItemName


class WL4Item(Item):
    game: str = "Wario Land 4"


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    quantity: int = 1


box_table = {
    # Entry Passage
    ItemName.entry_passage_jewel.nw: ItemData(57020, True),
    ItemName.entry_passage_jewel.ne: ItemData(57021, True),
    ItemName.entry_passage_jewel.sw: ItemData(57022, True),
    ItemName.entry_passage_jewel.se: ItemData(57023, True),
    # Emerald Passage
    ItemName.palm_tree_paradise.cd: ItemData(57000, False),
    ItemName.wildflower_fields.cd: ItemData(57001, False),
    ItemName.mystic_lake.cd: ItemData(57002, False),
    ItemName.monsoon_jungle.cd: ItemData(57003, False),
    ItemName.emerald_passage_jewel.nw: ItemData(57024, True, 4),
    ItemName.emerald_passage_jewel.ne: ItemData(57025, True, 4),
    ItemName.emerald_passage_jewel.sw: ItemData(57026, True, 4),
    ItemName.emerald_passage_jewel.se: ItemData(57027, True, 4),
    # Ruby Passage
    ItemName.curious_factory.cd: ItemData(57004, False),
    ItemName.toxic_landfill.cd: ItemData(57005, False),
    ItemName.forty_below_fridge.cd: ItemData(57006, False),
    ItemName.pinball_zone.cd: ItemData(57007, False),
    ItemName.ruby_passage_jewel.nw: ItemData(57028, True, 4),
    ItemName.ruby_passage_jewel.ne: ItemData(57029, True, 4),
    ItemName.ruby_passage_jewel.sw: ItemData(57030, True, 4),
    ItemName.ruby_passage_jewel.se: ItemData(57031, True, 4),
    # Topaz Passage
    ItemName.toy_block_tower.cd: ItemData(57008, False),
    ItemName.big_board.cd: ItemData(57009, False),
    ItemName.doodle_woods.cd: ItemData(57010, False),
    ItemName.domino_row.cd: ItemData(57011, False),
    ItemName.topaz_passage_jewel.nw: ItemData(57032, True, 4),
    ItemName.topaz_passage_jewel.ne: ItemData(57033, True, 4),
    ItemName.topaz_passage_jewel.sw: ItemData(57034, True, 4),
    ItemName.topaz_passage_jewel.se: ItemData(57035, True, 4),
    # Sapphire Passage
    ItemName.crescent_moon_village.cd: ItemData(57012, False),
    ItemName.arabian_night.cd: ItemData(57013, False),
    ItemName.fiery_cavern.cd: ItemData(57014, False),
    ItemName.hotel_horror.cd: ItemData(57015, False),
    ItemName.sapphire_passage_jewel.nw: ItemData(57036, True, 4),
    ItemName.sapphire_passage_jewel.ne: ItemData(57037, True, 4),
    ItemName.sapphire_passage_jewel.sw: ItemData(57038, True, 4),
    ItemName.sapphire_passage_jewel.se: ItemData(57039, True, 4),
    # Golden Pyramid
    ItemName.golden_pyramid_jewel.nw: ItemData(57040, True),
    ItemName.golden_pyramid_jewel.ne: ItemData(57041, True),
    ItemName.golden_pyramid_jewel.sw: ItemData(57042, True),
    ItemName.golden_pyramid_jewel.se: ItemData(57043, True),
    # Full Health Item
    ItemName.full_health: ItemData(57044, False, 17),
}

event_table = {
    ItemName.defeated_boss: ItemData(None, True),
    ItemName.victory: ItemData(None, True),
}

junk_table = {
    ItemName.health: ItemData(57200, False),
    ItemName.wario_form: ItemData(57201, False),
    ItemName.lightning: ItemData(57202, False),
}

# Unused placeholder for when Keyzers do get shuffled
keyzer_table = {
    ItemName.hall_of_hieroglyphs.keyzer: ItemData(57300, True),
    ItemName.palm_tree_paradise.keyzer: ItemData(57301, True),
    ItemName.wildflower_fields.keyzer: ItemData(57302, True),
    ItemName.mystic_lake.keyzer: ItemData(57303, True),
    ItemName.monsoon_jungle.keyzer: ItemData(57304, True),
    ItemName.curious_factory.keyzer: ItemData(57305, True),
    ItemName.toxic_landfill.keyzer: ItemData(57306, True),
    ItemName.forty_below_fridge.keyzer: ItemData(57307, True),
    ItemName.pinball_zone.keyzer: ItemData(57308, True),
    ItemName.toy_block_tower.keyzer: ItemData(57309, True),
    ItemName.big_board.keyzer: ItemData(57310, True),
    ItemName.doodle_woods.keyzer: ItemData(57311, True),
    ItemName.domino_row.keyzer: ItemData(57312, True),
    ItemName.crescent_moon_village.keyzer: ItemData(57313, True),
    ItemName.arabian_night.keyzer: ItemData(57314, True),
    ItemName.fiery_cavern.keyzer: ItemData(57315, True),
    ItemName.hotel_horror.keyzer: ItemData(57316, True),
    ItemName.golden_passage.keyzer: ItemData(57317, True),
}

item_table = {
    **box_table,
    **event_table,
    **junk_table,
}

lookup_id_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}
