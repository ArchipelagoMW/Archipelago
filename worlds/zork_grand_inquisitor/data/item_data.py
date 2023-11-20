from typing import Dict, NamedTuple, Optional, Tuple

from BaseClasses import ItemClassification

from ..enums import ZorkGrandInquisitorItems, ZorkGrandInquisitorTags


class ZorkGrandInquisitorItemData(NamedTuple):
    game_state_keys: Optional[Tuple[int, ...]]
    archipelago_id: Optional[int]
    classification: ItemClassification
    tags: Tuple[ZorkGrandInquisitorTags, ...]
    maximum_quantity: Optional[int] = 1


ITEM_OFFSET = 9758067000

item_data: Dict[ZorkGrandInquisitorItems, ZorkGrandInquisitorItemData] = {
    # Inventory Items
    ZorkGrandInquisitorItems.FLATHEADIA_FUDGE: ZorkGrandInquisitorItemData(
        game_state_keys=(54,),
        archipelago_id=ITEM_OFFSET + 0,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.HAMMER: ZorkGrandInquisitorItemData(
        game_state_keys=(23,),
        archipelago_id=ITEM_OFFSET + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.HUNGUS_LARD: ZorkGrandInquisitorItemData(
        game_state_keys=(55,),
        archipelago_id=ITEM_OFFSET + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.JAR_OF_HOTBUGS: ZorkGrandInquisitorItemData(
        game_state_keys=(56,),
        archipelago_id=ITEM_OFFSET + 3,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.LANTERN: ZorkGrandInquisitorItemData(
        game_state_keys=(4,),
        archipelago_id=ITEM_OFFSET + 4,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER: ZorkGrandInquisitorItemData(
        game_state_keys=(88,),
        archipelago_id=ITEM_OFFSET + 5,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.LETTER_OPENER: ZorkGrandInquisitorItemData(
        game_state_keys=(64,),
        archipelago_id=ITEM_OFFSET + 6,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.MEAD_LIGHT: ZorkGrandInquisitorItemData(
        game_state_keys=(2,),
        archipelago_id=ITEM_OFFSET + 7,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.MOSS_OF_MAREILON: ZorkGrandInquisitorItemData(
        game_state_keys=(57,),
        archipelago_id=ITEM_OFFSET + 8,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.MUG: ZorkGrandInquisitorItemData(
        game_state_keys=(35,),
        archipelago_id=ITEM_OFFSET + 9,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.OLD_SCRATCH_CARD: ZorkGrandInquisitorItemData(
        game_state_keys=(17,),
        archipelago_id=ITEM_OFFSET + 10,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.PERMA_SUCK_MACHINE: ZorkGrandInquisitorItemData(
        game_state_keys=(36,),
        archipelago_id=ITEM_OFFSET + 11,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.PLASTIC_SIX_PACK_HOLDER: ZorkGrandInquisitorItemData(
        game_state_keys=(3,),
        archipelago_id=ITEM_OFFSET + 12,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS: ZorkGrandInquisitorItemData(
        game_state_keys=(5827,),
        archipelago_id=ITEM_OFFSET + 13,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.PROZORK_TABLET: ZorkGrandInquisitorItemData(
        game_state_keys=(65,),
        archipelago_id=ITEM_OFFSET + 14,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.QUELBEE_HONEYCOMB: ZorkGrandInquisitorItemData(
        game_state_keys=(53,),
        archipelago_id=ITEM_OFFSET + 15,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.ROPE: ZorkGrandInquisitorItemData(
        game_state_keys=(83,),
        archipelago_id=ITEM_OFFSET + 16,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.SHOVEL: ZorkGrandInquisitorItemData(
        game_state_keys=(49,),
        archipelago_id=ITEM_OFFSET + 17,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.SNAPDRAGON: ZorkGrandInquisitorItemData(
        game_state_keys=(50,),
        archipelago_id=ITEM_OFFSET + 18,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.STUDENT_ID: ZorkGrandInquisitorItemData(
        game_state_keys=(39,),
        archipelago_id=ITEM_OFFSET + 19,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.SUBWAY_TOKEN: ZorkGrandInquisitorItemData(
        game_state_keys=(20,),
        archipelago_id=ITEM_OFFSET + 20,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.ZIMDOR_SCROLL: ZorkGrandInquisitorItemData(
        game_state_keys=(25,),
        archipelago_id=ITEM_OFFSET + 21,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.ZORK_ROCKS: ZorkGrandInquisitorItemData(
        game_state_keys=(37,),
        archipelago_id=ITEM_OFFSET + 22,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    # Revealed
    ZorkGrandInquisitorItems.REVEALED_BROGS_TIME_TUNNEL_ITEMS: ZorkGrandInquisitorItemData(
        game_state_keys=(15065, 15088, 2628),
        archipelago_id=ITEM_OFFSET + 100 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.REVEALED,),
    ),
    ZorkGrandInquisitorItems.REVEALED_GRIFFS_TIME_TUNNEL_ITEMS: ZorkGrandInquisitorItemData(
        game_state_keys=(1340, 1341, 1477, 1814),
        archipelago_id=ITEM_OFFSET + 100 + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.REVEALED,),
    ),
    ZorkGrandInquisitorItems.REVEALED_LUCYS_TIME_TUNNEL_ITEMS: ZorkGrandInquisitorItemData(
        game_state_keys=(15405,),
        archipelago_id=ITEM_OFFSET + 100 + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.REVEALED,),
    ),
    # Unlocked
    ZorkGrandInquisitorItems.UNLOCKED_BLANK_SCROLL_BOX_ACCESS: ZorkGrandInquisitorItemData(
        game_state_keys=(12095,),
        archipelago_id=ITEM_OFFSET + 200 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.UNLOCKED,),
    ),
    # Spells
    ZorkGrandInquisitorItems.SPELL_GLORF: ZorkGrandInquisitorItemData(
        game_state_keys=(202,),
        archipelago_id=ITEM_OFFSET + 300 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_GOLGATEM: ZorkGrandInquisitorItemData(
        game_state_keys=(192,),
        archipelago_id=ITEM_OFFSET + 300 + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_IGRAM: ZorkGrandInquisitorItemData(
        game_state_keys=(199,),
        archipelago_id=ITEM_OFFSET + 300 + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_KENDALL: ZorkGrandInquisitorItemData(
        game_state_keys=(196,),
        archipelago_id=ITEM_OFFSET + 300 + 3,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_NARWILE: ZorkGrandInquisitorItemData(
        game_state_keys=(197,),
        archipelago_id=ITEM_OFFSET + 300 + 4,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_OBIDIL: ZorkGrandInquisitorItemData(
        game_state_keys=(193,),
        archipelago_id=ITEM_OFFSET + 300 + 5,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_REZROV: ZorkGrandInquisitorItemData(
        game_state_keys=(195,),
        archipelago_id=ITEM_OFFSET + 300 + 6,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_THROCK: ZorkGrandInquisitorItemData(
        game_state_keys=(200,),
        archipelago_id=ITEM_OFFSET + 300 + 7,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_VOXAM: ZorkGrandInquisitorItemData(
        game_state_keys=(191,),
        archipelago_id=ITEM_OFFSET + 300 + 8,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_YASTARD: ZorkGrandInquisitorItemData(
        game_state_keys=(198,),
        archipelago_id=ITEM_OFFSET + 300 + 9,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    # Subway Destinations
    ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM: ZorkGrandInquisitorItemData(
        game_state_keys=None,  # This is more complicated. Will be handled in GameController
        archipelago_id=ITEM_OFFSET + 400 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SUBWAY_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES: ZorkGrandInquisitorItemData(
        game_state_keys=None,  # This is more complicated. Will be handled in GameController
        archipelago_id=ITEM_OFFSET + 400 + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SUBWAY_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY: ZorkGrandInquisitorItemData(
        game_state_keys=None,  # This is more complicated. Will be handled in GameController
        archipelago_id=ITEM_OFFSET + 400 + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SUBWAY_DESTINATION,),
    ),
    # Teleporter Destinations
    ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR: ZorkGrandInquisitorItemData(
        game_state_keys=(2203,),
        archipelago_id=ITEM_OFFSET + 500 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TELEPORTER_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH: ZorkGrandInquisitorItemData(
        game_state_keys=(7132,),
        archipelago_id=ITEM_OFFSET + 500 + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TELEPORTER_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES: ZorkGrandInquisitorItemData(
        game_state_keys=(7119,),
        archipelago_id=ITEM_OFFSET + 500 + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TELEPORTER_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY: ZorkGrandInquisitorItemData(
        game_state_keys=(7148,),
        archipelago_id=ITEM_OFFSET + 500 + 3,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TELEPORTER_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB: ZorkGrandInquisitorItemData(
        game_state_keys=(16545,),
        archipelago_id=ITEM_OFFSET + 500 + 4,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TELEPORTER_DESTINATION,),
    ),
    # Totems
    ZorkGrandInquisitorItems.TOTEM_BROG: ZorkGrandInquisitorItemData(
        game_state_keys=(4853,),
        archipelago_id=ITEM_OFFSET + 600 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TOTEM,),
    ),
    ZorkGrandInquisitorItems.TOTEM_GRIFF: ZorkGrandInquisitorItemData(
        game_state_keys=(4315,),
        archipelago_id=ITEM_OFFSET + 600 + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TOTEM,),
    ),
    ZorkGrandInquisitorItems.TOTEM_LUCY: ZorkGrandInquisitorItemData(
        game_state_keys=(5223,),
        archipelago_id=ITEM_OFFSET + 600 + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TOTEM,),
    ),
    # Filler
    ZorkGrandInquisitorItems.FILLER_INQUISITION_PROPAGANDA_FLYER: ZorkGrandInquisitorItemData(
        game_state_keys=None,
        archipelago_id=ITEM_OFFSET + 700 + 0,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.FILLER,),
        maximum_quantity=None,
    ),
    ZorkGrandInquisitorItems.FILLER_UNREADABLE_SPELL_SCROLL: ZorkGrandInquisitorItemData(
        game_state_keys=None,
        archipelago_id=ITEM_OFFSET + 700 + 1,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.FILLER,),
        maximum_quantity=None,
    ),
    ZorkGrandInquisitorItems.FILLER_MAGIC_CONTRABAND: ZorkGrandInquisitorItemData(
        game_state_keys=None,
        archipelago_id=ITEM_OFFSET + 700 + 2,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.FILLER,),
        maximum_quantity=None,
    ),
    ZorkGrandInquisitorItems.FILLER_FROBOZZ_ELECTRIC_GADGET: ZorkGrandInquisitorItemData(
        game_state_keys=None,
        archipelago_id=ITEM_OFFSET + 700 + 3,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.FILLER,),
        maximum_quantity=None,
    ),
    ZorkGrandInquisitorItems.FILLER_NONSENSICAL_INQUISITION_PAPERWORK: ZorkGrandInquisitorItemData(
        game_state_keys=None,
        archipelago_id=ITEM_OFFSET + 700 + 4,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.FILLER,),
        maximum_quantity=None,
    ),
    # Traps
    # ...
}
