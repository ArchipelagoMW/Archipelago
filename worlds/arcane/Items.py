import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool = True
    quantity: int = 1
    event: bool = False


class ArcaneItem(Item):
    game: str = "Arcane"


# Separate tables for each type of item.

junk_table = {
    ItemName.s1e1_key:     ItemData(0xACA002, False),
}

main_table = {
    # S1E1 Items
    ItemName.s1e1_matches: ItemData(0xACA001, True),
    ItemName.s1e1_hook:    ItemData(0xACA003, True),

    # S1E2 Items
    ItemName.s1e2_newspaper: ItemData(0xACA004, True),
    ItemName.s1e2_key:       ItemData(0xACA005, True),

    # S1E3 Items
    ItemName.s1e3_diamond:    ItemData(0xACA006, True, 2),
    ItemName.s1e3_platter:    ItemData(0xACA007, True),
    ItemName.s1e3_candelabra: ItemData(0xACA008, True),
    ItemName.s1e3_crowbar:    ItemData(0xACA009, True),

    # S1E4 Items
    ItemName.s1e4_ladder: ItemData(0xACA00A, True),
    ItemName.s1e4_gun:    ItemData(0xACA00B, True),
    ItemName.s1e4_map:    ItemData(0xACA00C, False),
    ItemName.note_l:      ItemData(0xACA00D, True),
    ItemName.note_r:      ItemData(0xACA00E, True),
    ItemName.dagger:      ItemData(0xACA00F, True),
    ItemName.seth:        ItemData(0xACA010, True),
    ItemName.idol:        ItemData(0xACA011, True),

    # S2E1 Items
    ItemName.s2e1_pallet:   ItemData(0xACA012, True),
    ItemName.s2e1_wrench:   ItemData(0xACA013, True),
    ItemName.s2e1_dcatcher: ItemData(0xACA014, False),
    ItemName.s2e1_note_a:   ItemData(0xACA015, False),
    ItemName.s2e1_crowbar:  ItemData(0xACA016, True),
    ItemName.s2e1_hook:     ItemData(0xACA017, False),
    ItemName.s2e1_note_f:   ItemData(0xACA018, False),
    ItemName.s2e1_cylinder: ItemData(0xACA019, True),

    # S2E2 Items
    ItemName.s2e2_note:       ItemData(0xACA01A, False),
    ItemName.s2e2_lighter:    ItemData(0xACA01B, True),
    ItemName.s2e2_candelabra: ItemData(0xACA01C, True),
    ItemName.s2e2_key:        ItemData(0xACA01D, True),
    ItemName.s2e2_handle:     ItemData(0xACA01E, True),

    # S2E3 Items
    ItemName.s2e3_buoy:    ItemData(0xACA01F, True),
    ItemName.s2e3_oars:    ItemData(0xACA020, True),
    ItemName.s2e3_cleaner: ItemData(0xACA021, True),
    ItemName.s2e3_hammer:  ItemData(0xACA022, True),
    ItemName.s2e3_book:    ItemData(0xACA023, False),
    ItemName.s2e3_helmet:  ItemData(0xACA024, True),

    # S2E4 Items
    ItemName.s2e4_matches:     ItemData(0xACA025, True),
    ItemName.s2e4_bucket:      ItemData(0xACA026, True),
    ItemName.s2e4_bottle:      ItemData(0xACA027, True),
    ItemName.s2e4_stethoscope: ItemData(0xACA028, True),
    ItemName.s2e4_frog:        ItemData(0xACA029, True),
    ItemName.s2e4_ruby:        ItemData(0xACA02A, True),
    ItemName.s2e4_letter:      ItemData(0xACA02B, False),
    ItemName.s2e4_amulet:      ItemData(0xACA02C, True),
    ItemName.s2e4_alazif:      ItemData(0xACA02D, True),

    # S2E5 Items
    ItemName.s2e5_note:  ItemData(0xACA02E, False),
    ItemName.s2e5_book:  ItemData(0xACA02F, False),
    ItemName.s2e5_slice: ItemData(0xACA030, True, 4),

    # S2E6 Items
    ItemName.s2e6_urn:     ItemData(0xACA031, True),
    ItemName.s2e6_circlet: ItemData(0xACA032, True),
    ItemName.s2e6_matches: ItemData(0xACA033, False),
    ItemName.s2e6_book:    ItemData(0xACA034, True),
    ItemName.s2e6_card:    ItemData(0xACA035, True, 3),

    # S2E7 Items
    ItemName.s2e7_rope:     ItemData(0xACA036, True),
    ItemName.s2e7_bird:     ItemData(0xACA037, True),
    ItemName.s2e7_cross:    ItemData(0xACA038, True),
    ItemName.s2e7_crossbow: ItemData(0xACA039, True),
    ItemName.s2e7_arrows:   ItemData(0xACA03A, True),
    ItemName.s2e7_scroll1:  ItemData(0xACA03B, False),
    ItemName.s2e7_scroll2:  ItemData(0xACA03C, False),

    # S2E8 Items
    ItemName.s2e8_shovel:  ItemData(0xACA03D, True),
    ItemName.s2e8_towhook: ItemData(0xACA03E, True),
    ItemName.s2e8_chalk:   ItemData(0xACA03F, True),
    ItemName.s2e8_slab_s:  ItemData(0xACA040, True),
    ItemName.s2e8_slab_c:  ItemData(0xACA041, True),
    ItemName.hand:         ItemData(0xACA042, True, 2),
    ItemName.legs:         ItemData(0xACA043, True),
    ItemName.wing:         ItemData(0xACA044, True, 2),
    ItemName.heart:        ItemData(0xACA045, True),
    ItemName.eyes:         ItemData(0xACA046, True),
    ItemName.yhe:          ItemData(0xACA047, True),
    ItemName.ibinoculars:  ItemData(0xACA048, True),
}

event_table = {
    ItemName.clear: ItemData(None, True, event=True),
}

# Complete item table.
item_table = {
    **junk_table,
    **main_table,
    **event_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
