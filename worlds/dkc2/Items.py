import typing

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from .Names import ItemName

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    trap: bool = False
    quantity: int = 1

STARTING_ID = 0xBF0000

class DKC2Item(Item):
    game = "Donkey Kong Country 2"

# Item tables
event_table = {
    ItemName.victory:           ItemData(STARTING_ID + 0x0000, True),
}

worlds_table = {
    ItemName.gangplank_galleon:     ItemData(STARTING_ID + 0x0001, True),
    ItemName.crocodile_cauldron:    ItemData(STARTING_ID + 0x0002, True),
    ItemName.krem_quay:             ItemData(STARTING_ID + 0x0003, True),
    ItemName.krazy_kremland:        ItemData(STARTING_ID + 0x0004, True),
    ItemName.gloomy_gulch:          ItemData(STARTING_ID + 0x0005, True),
    ItemName.krools_keep:           ItemData(STARTING_ID + 0x0006, True),
    ItemName.the_flying_krock:      ItemData(STARTING_ID + 0x0007, True),
}

mcguffin_table = {
    ItemName.lost_world_rock:       ItemData(STARTING_ID + 0x0008, True),
    ItemName.dk_coin:               ItemData(STARTING_ID + 0x0009, False),
    ItemName.kremkoins:             ItemData(STARTING_ID + 0x000A, False),
}

lost_world_table = {
    ItemName.lost_world_cauldron:   ItemData(STARTING_ID + 0x000B, True),
    ItemName.lost_world_quay:       ItemData(STARTING_ID + 0x000C, True),
    ItemName.lost_world_kremland:   ItemData(STARTING_ID + 0x000D, True),
    ItemName.lost_world_gulch:      ItemData(STARTING_ID + 0x000E, True),
    ItemName.lost_world_keep:       ItemData(STARTING_ID + 0x000F, True),
}

progression_table = {
    ItemName.diddy:                 ItemData(STARTING_ID + 0x0010, True),
    ItemName.dixie:                 ItemData(STARTING_ID + 0x0011, True),
    ItemName.carry:                 ItemData(STARTING_ID + 0x0012, True),
    ItemName.climb:                 ItemData(STARTING_ID + 0x0013, True),
    ItemName.cling:                 ItemData(STARTING_ID + 0x0014, True),
    ItemName.cartwheel:             ItemData(STARTING_ID + 0x0015, True),
    ItemName.swim:                  ItemData(STARTING_ID + 0x0016, True),
    ItemName.team_attack:           ItemData(STARTING_ID + 0x0017, True),
    ItemName.helicopter_spin:       ItemData(STARTING_ID + 0x0018, True),
    ItemName.rambi:                 ItemData(STARTING_ID + 0x0019, True),
    ItemName.squawks:               ItemData(STARTING_ID + 0x001A, True),
    ItemName.enguarde:              ItemData(STARTING_ID + 0x001B, True),
    ItemName.squitter:              ItemData(STARTING_ID + 0x001C, True),
    ItemName.rattly:                ItemData(STARTING_ID + 0x001D, True),
    ItemName.clapper:               ItemData(STARTING_ID + 0x001E, True),
    ItemName.glimmer:               ItemData(STARTING_ID + 0x001F, True),
    ItemName.barrel_kannons:        ItemData(STARTING_ID + 0x0020, True),
    ItemName.barrel_exclamation:    ItemData(STARTING_ID + 0x0021, True),
    ItemName.barrel_kong:           ItemData(STARTING_ID + 0x0022, True),
    ItemName.barrel_warp:           ItemData(STARTING_ID + 0x0023, True),
    ItemName.barrel_control:        ItemData(STARTING_ID + 0x0024, True),
    ItemName.skull_kart:            ItemData(STARTING_ID + 0x0025, True),
}

junk_table = {
    ItemName.banana_coin:           ItemData(STARTING_ID + 0x0030, False),
    ItemName.red_balloon:           ItemData(STARTING_ID + 0x0031, False),
}

trap_table = {
    ItemName.freeze_trap:           ItemData(STARTING_ID + 0x0040, False, True),
    ItemName.reverse_trap:          ItemData(STARTING_ID + 0x0041, False, True),
}

item_groups = {
    "Worlds": {
        ItemName.gangplank_galleon,
        ItemName.crocodile_cauldron,
        ItemName.krem_quay,
        ItemName.krazy_kremland,
        ItemName.gloomy_gulch,
        ItemName.krools_keep,
        ItemName.the_flying_krock,
    },
    "Lost World": {
        ItemName.lost_world_cauldron,
        ItemName.lost_world_quay,
        ItemName.lost_world_kremland,
        ItemName.lost_world_gulch,
        ItemName.lost_world_keep,
    },
    "Abilities": {
        ItemName.carry,
        ItemName.climb,
        ItemName.cling,
        ItemName.cartwheel,
        ItemName.swim,
        ItemName.team_attack,
        ItemName.helicopter_spin,
    },
    "Animals": {
        ItemName.rambi,
        ItemName.squawks,
        ItemName.enguarde,
        ItemName.squitter,
        ItemName.rattly,
        ItemName.clapper,
        ItemName.glimmer,
        ItemName.skull_kart,
    },
    "Barrels": {
        ItemName.barrel_kannons,
        ItemName.barrel_exclamation,
        ItemName.barrel_kong,
        ItemName.barrel_warp,
        ItemName.barrel_control,
    }
}

item_table = {
    **event_table,
    **mcguffin_table,
    **worlds_table,
    **lost_world_table,
    **progression_table,
    **trap_table,
    **junk_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}